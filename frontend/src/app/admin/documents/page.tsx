"use client";

import { useState, useEffect, useRef } from "react";
import {
  Upload, Search, RefreshCw, Filter, Layers, CheckCircle2,
  Loader2, AlertTriangle, Clock, FileText, Trash2, Eye, Info,
  ChevronLeft, ChevronRight,
} from "lucide-react";
import { UploadDocumentModal } from "@/components/admin/UploadDocumentModal";
import { DocumentMetadataModal } from "@/components/admin/DocumentMetadataModal";
import { fetchWithAuth } from "@/lib/api";

export interface DocumentItem {
  id: string;
  title: string;
  category: string;
  status: string;
  chunk_count?: number;
  file_url?: string;
  file_name?: string;
  created_at?: string;
  updated_at?: string;
  description?: string;
}

type ToastType = "success" | "error";
const PAGE_SIZE = 10;

export default function AdminDocumentsPage() {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("All");
  const [statusFilter, setStatusFilter] = useState("All");
  const [sortBy, setSortBy] = useState<"newest" | "title" | "chunks">("newest");
  const [page, setPage] = useState(1);
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [selectedDoc, setSelectedDoc] = useState<DocumentItem | null>(null);
  const [toast, setToast] = useState<{ type: ToastType; msg: string } | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [reprocessingId, setReprocessingId] = useState<string | null>(null);
  const toastTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const showToast = (type: ToastType, msg: string) => {
    setToast({ type, msg });
    if (toastTimer.current) clearTimeout(toastTimer.current);
    toastTimer.current = setTimeout(() => setToast(null), 4000);
  };

  const loadDocuments = async () => {
    setLoading(true);
    try {
      const data = await fetchWithAuth("/documents/");
      if (data?.documents) {
        setDocuments(
          data.documents.map((d: any) => ({
            id: d.id,
            title: d.title || d.name || "Untitled",
            category: d.category || "General",
            status: d.status || "uploaded",
            chunk_count: d.chunk_count || 0,
            file_url: d.file_url,
            file_name: d.file_name,
            created_at: d.created_at,
            updated_at: d.updated_at,
            description: d.description,
          }))
        );
      }
    } catch {
      showToast("error", "Failed to load documents.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadDocuments(); }, []);

  const handleDelete = async (id: string) => {
    if (!confirm("Delete this document? This will remove the PDF from storage and all vectors from Pinecone.")) return;
    setDeletingId(id);
    try {
      await fetchWithAuth(`/documents/${id}`, { method: "DELETE" });
      setDocuments((prev) => prev.filter((d) => d.id !== id));
      showToast("success", "Document deleted successfully.");
    } catch {
      showToast("error", "Failed to delete document.");
    } finally {
      setDeletingId(null);
    }
  };

  const handleReprocess = async (id: string) => {
    setReprocessingId(id);
    setDocuments((prev) => prev.map((d) => d.id === id ? { ...d, status: "uploaded" } : d));
    try {
      const res = await fetchWithAuth(`/documents/${id}/reprocess`, { method: "POST" });
      if (res?.status === "success") {
        showToast("success", "Reprocessing started. Document will be re-indexed shortly.");
        // Poll for completion after 8s
        setTimeout(() => loadDocuments(), 8000);
      } else {
        showToast("error", res?.message || "Reprocessing failed.");
        loadDocuments();
      }
    } catch {
      showToast("error", "Reprocessing failed. Check backend logs.");
      loadDocuments();
    } finally {
      setReprocessingId(null);
    }
  };

  // Filter + sort
  const filtered = documents
    .filter((d) => {
      const q = searchQuery.toLowerCase();
      const matchQ = d.title.toLowerCase().includes(q) || d.category.toLowerCase().includes(q);
      const matchCat = categoryFilter === "All" || d.category === categoryFilter;
      const matchSt = statusFilter === "All" || d.status === statusFilter;
      return matchQ && matchCat && matchSt;
    })
    .sort((a, b) => {
      if (sortBy === "title") return a.title.localeCompare(b.title);
      if (sortBy === "chunks") return (b.chunk_count || 0) - (a.chunk_count || 0);
      return new Date(b.created_at || 0).getTime() - new Date(a.created_at || 0).getTime();
    });

  const totalPages = Math.ceil(filtered.length / PAGE_SIZE);
  const paginated = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);
  const processingCount = documents.filter((d) => d.status === "processing").length;

  const categories = ["All", ...Array.from(new Set(documents.map((d) => d.category))).sort()];

  const statusBadge = (s: string) => {
    switch (s) {
      case "indexed":    return { cls: "bg-emerald-50 text-emerald-700 border-emerald-200", icon: <CheckCircle2 className="h-3 w-3" />, label: "Indexed" };
      case "processing": return { cls: "bg-amber-50 text-amber-700 border-amber-200", icon: <Loader2 className="h-3 w-3 animate-spin" />, label: "Processing" };
      case "failed":     return { cls: "bg-rose-50 text-rose-700 border-rose-200", icon: <AlertTriangle className="h-3 w-3" />, label: "Failed" };
      default:           return { cls: "bg-slate-100 text-slate-600 border-slate-200", icon: <Clock className="h-3 w-3" />, label: "Uploaded" };
    }
  };

  return (
    <div className="p-8 space-y-6 animate-fade-in">
      {toast && (
        <div className={`fixed top-6 right-6 z-50 flex items-center gap-2 rounded-xl px-5 py-3 text-sm font-semibold text-white shadow-2xl animate-fade-in ${toast.type === "success" ? "bg-emerald-600" : "bg-rose-600"}`}>
          <CheckCircle2 className="h-4 w-4 shrink-0" /> {toast.msg}
        </div>
      )}

      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Documents Management</h1>
          <p className="mt-1 text-slate-500 text-sm">Manage knowledge base PDFs and Pinecone vector indexing</p>
        </div>
        <div className="flex items-center gap-3">
          <button onClick={loadDocuments}
            className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 transition">
            <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} /> Refresh
          </button>
          <button onClick={() => setIsUploadOpen(true)}
            className="inline-flex items-center gap-2 rounded-xl bg-nexora-700 px-4 py-2.5 text-sm font-semibold text-white hover:bg-nexora-800 transition shadow-md">
            <Upload className="h-4 w-4" /> Upload Document
          </button>
        </div>
      </div>

      {/* Processing Banner */}
      {processingCount > 0 && (
        <div className="rounded-xl bg-amber-50 border border-amber-200 p-4 flex items-center gap-3">
          <Loader2 className="h-5 w-5 text-amber-600 animate-spin shrink-0" />
          <div className="flex-1">
            <p className="text-sm font-bold text-amber-800">
              {processingCount} document{processingCount > 1 ? "s" : ""} being indexed into Pinecone…
            </p>
            <div className="mt-1.5 h-1.5 w-full rounded-full bg-amber-200 overflow-hidden">
              <div className="h-full bg-amber-600 w-2/3 animate-pulse rounded-full" />
            </div>
          </div>
        </div>
      )}

      {/* Stats Row */}
      <div className="grid gap-4 grid-cols-2 sm:grid-cols-4">
        {[
          { label: "Total", value: documents.length, color: "text-slate-900" },
          { label: "Indexed", value: documents.filter((d) => d.status === "indexed").length, color: "text-emerald-700" },
          { label: "Processing", value: documents.filter((d) => d.status === "processing").length, color: "text-amber-700" },
          { label: "Failed", value: documents.filter((d) => d.status === "failed").length, color: "text-rose-700" },
        ].map((s) => (
          <div key={s.label} className="os-card p-4 text-center">
            <p className={`text-2xl font-extrabold ${s.color}`}>{s.value}</p>
            <p className="text-xs text-slate-400 font-semibold mt-0.5">{s.label}</p>
          </div>
        ))}
      </div>

      {/* Search + Filters */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center flex-wrap">
        <div className="relative flex-1 min-w-48">
          <Search className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <input type="text" value={searchQuery} onChange={(e) => { setSearchQuery(e.target.value); setPage(1); }}
            placeholder="Search by title or category..."
            className="w-full rounded-xl border border-slate-200 py-2.5 pl-10 pr-4 text-sm focus:border-nexora-500 focus:outline-none" />
        </div>
        <div className="flex items-center gap-2 flex-wrap">
          <Filter className="h-4 w-4 text-slate-400" />
          <select value={categoryFilter} onChange={(e) => { setCategoryFilter(e.target.value); setPage(1); }}
            className="rounded-xl border border-slate-200 px-3 py-2.5 text-sm bg-white focus:outline-none">
            {categories.map((c) => <option key={c} value={c}>{c === "All" ? "All Categories" : c}</option>)}
          </select>
          <select value={statusFilter} onChange={(e) => { setStatusFilter(e.target.value); setPage(1); }}
            className="rounded-xl border border-slate-200 px-3 py-2.5 text-sm bg-white focus:outline-none">
            {["All", "indexed", "processing", "uploaded", "failed"].map((s) => (
              <option key={s} value={s}>{s === "All" ? "All Statuses" : s.charAt(0).toUpperCase() + s.slice(1)}</option>
            ))}
          </select>
          <select value={sortBy} onChange={(e) => setSortBy(e.target.value as any)}
            className="rounded-xl border border-slate-200 px-3 py-2.5 text-sm bg-white focus:outline-none">
            <option value="newest">Newest First</option>
            <option value="title">Title A–Z</option>
            <option value="chunks">Most Chunks</option>
          </select>
        </div>
      </div>

      {/* Document List */}
      <div className="space-y-2.5">
        {loading ? (
          <div className="os-card p-10 text-center">
            <Loader2 className="h-7 w-7 animate-spin mx-auto text-nexora-600 mb-3" />
            <p className="text-sm text-slate-400 font-medium">Loading documents…</p>
          </div>
        ) : paginated.length === 0 ? (
          <div className="os-card p-10 text-center">
            <FileText className="h-10 w-10 text-slate-200 mx-auto mb-3" />
            <p className="font-semibold text-slate-700">No documents found</p>
            <p className="text-xs text-slate-400 mt-1">Upload a PDF or adjust your filters.</p>
          </div>
        ) : (
          paginated.map((doc) => {
            const badge = statusBadge(doc.status);
            return (
              <div key={doc.id} className="os-card p-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <div className="flex items-start gap-3 flex-1 min-w-0">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-nexora-50 text-nexora-600">
                    <FileText className="h-5 w-5" />
                  </div>
                  <div className="min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <h3 className="font-semibold text-slate-900 truncate">{doc.title}</h3>
                      <span className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-bold border ${badge.cls}`}>
                        {badge.icon} {badge.label}
                      </span>
                    </div>
                    <div className="flex items-center gap-3 mt-1 text-xs text-slate-400 flex-wrap">
                      <span className="rounded-full bg-slate-100 px-2 py-0.5 font-medium text-slate-600">{doc.category}</span>
                      {(doc.chunk_count || 0) > 0 && (
                        <span className="flex items-center gap-1 text-nexora-600 font-semibold">
                          <Layers className="h-3 w-3" /> {doc.chunk_count} chunks
                        </span>
                      )}
                      {doc.created_at && (
                        <span>{new Date(doc.created_at).toLocaleDateString()}</span>
                      )}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2 flex-wrap shrink-0">
                  <button onClick={() => setSelectedDoc(doc)}
                    className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50 transition">
                    <Info className="h-3.5 w-3.5 inline mr-1" />Metadata
                  </button>
                  {doc.file_url && (
                    <a href={doc.file_url} target="_blank" rel="noopener noreferrer"
                      className="rounded-lg border border-nexora-200 bg-nexora-50 px-3 py-1.5 text-xs font-medium text-nexora-700 hover:bg-nexora-100 transition inline-flex items-center gap-1">
                      <Eye className="h-3.5 w-3.5" /> View
                    </a>
                  )}
                  <button onClick={() => handleReprocess(doc.id)} disabled={reprocessingId === doc.id || doc.status === "processing"}
                    className="rounded-lg border border-amber-200 bg-amber-50 px-3 py-1.5 text-xs font-medium text-amber-700 hover:bg-amber-100 transition disabled:opacity-50">
                    {reprocessingId === doc.id ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : "Reprocess"}
                  </button>
                  <button onClick={() => handleDelete(doc.id)} disabled={deletingId === doc.id}
                    className="rounded-lg border border-rose-200 px-3 py-1.5 text-xs font-medium text-rose-600 hover:bg-rose-50 transition disabled:opacity-50">
                    {deletingId === doc.id ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Trash2 className="h-3.5 w-3.5" />}
                  </button>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between pt-2">
          <p className="text-xs text-slate-400">
            Showing {(page - 1) * PAGE_SIZE + 1}–{Math.min(page * PAGE_SIZE, filtered.length)} of {filtered.length}
          </p>
          <div className="flex items-center gap-2">
            <button onClick={() => setPage((p) => Math.max(1, p - 1))} disabled={page === 1}
              className="rounded-lg border border-slate-200 p-2 text-slate-500 hover:bg-slate-50 disabled:opacity-40 transition">
              <ChevronLeft className="h-4 w-4" />
            </button>
            <span className="text-xs font-semibold text-slate-700">Page {page} / {totalPages}</span>
            <button onClick={() => setPage((p) => Math.min(totalPages, p + 1))} disabled={page === totalPages}
              className="rounded-lg border border-slate-200 p-2 text-slate-500 hover:bg-slate-50 disabled:opacity-40 transition">
              <ChevronRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

      <UploadDocumentModal
        isOpen={isUploadOpen}
        onClose={() => setIsUploadOpen(false)}
        onSuccess={() => { loadDocuments(); showToast("success", "PDF uploaded. Background indexing started."); }}
      />

      <DocumentMetadataModal
        isOpen={!!selectedDoc}
        onClose={() => setSelectedDoc(null)}
        document={selectedDoc}
        onReprocess={(id) => { setSelectedDoc(null); handleReprocess(id); }}
      />
    </div>
  );
}
