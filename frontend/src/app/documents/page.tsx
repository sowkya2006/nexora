"use client";

import { useState, useEffect } from "react";
import { DocumentCard } from "@/components/ui/DocumentCard";
import { documents as mockDocuments, Document } from "@/lib/data";
import { DOCUMENT_CATEGORIES } from "@/lib/constants";
import { Search, Loader2, FileText, Filter } from "lucide-react";

export default function DocumentsPage() {
  const [docList, setDocList] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("All");

  const loadDocuments = async () => {
    setLoading(true);
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
      const res = await fetch(`${API_URL}/documents/`);
      if (res.ok) {
        const data = await res.json();
        if (data && data.documents && data.documents.length > 0) {
          const mapped: Document[] = data.documents.map((d: any) => ({
            id: d.id,
            name: d.title || d.name || "Untitled Document",
            category: d.category || "General",
            description: d.description || "Official document from Nexora University.",
            version: d.created_at ? new Date(d.created_at).getFullYear().toString() : "2026",
            updatedAt: d.created_at ? new Date(d.created_at).toISOString().split("T")[0] : "2026-07-01",
            fileUrl: d.file_url || (d.file_name
              ? `http://localhost:8000/knowledge_base/${d.file_name.replace(/^[a-f0-9\-]+_/, "")}`
              : undefined),
            file_name: d.file_name,
            pages: d.pages || 12,
            size: d.size || "1.4 MB",
            status: d.status || "indexed",
          }));
          setDocList(mapped);
          setLoading(false);
          return;
        }
      }
    } catch (err) {
      console.warn("Failed to fetch documents from API, falling back to local list:", err);
    }
    setDocList(mockDocuments);
    setLoading(false);
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  const filtered = docList.filter((d) => {
    const matchesQuery =
      d.name.toLowerCase().includes(query.toLowerCase()) ||
      d.description.toLowerCase().includes(query.toLowerCase());
    const matchesCategory = category === "All" || d.category === category;
    return matchesQuery && matchesCategory;
  });

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header Banner Widget */}
      <div className="os-card-static p-6 md:p-8 bg-gradient-to-br from-slate-900 via-nexora-900 to-nexora-950 text-white flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 rounded-full bg-nexora-800/60 px-3 py-1 text-xs font-bold text-nexora-200 border border-nexora-500/30">
            <FileText className="h-4 w-4 text-nexora-300" />
            <span>Official Knowledge Base</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">University Document Library</h1>
          <p className="text-xs sm:text-sm text-slate-300 max-w-xl">
            Access official university handbooks, fee regulations, academic calendars, and policy guidelines.
          </p>
        </div>

        <div className="flex items-center gap-2 bg-white/10 p-3 rounded-2xl border border-white/15 backdrop-blur-md shrink-0 text-xs">
          <span className="font-extrabold text-xl text-emerald-400">{docList.length}</span>
          <span className="text-slate-300 font-medium leading-tight">PDF Documents<br/>Indexed in RAG</span>
        </div>
      </div>

      {/* Filter & Search Controls */}
      <div className="os-card p-4 flex flex-col gap-3 sm:flex-row items-center">
        <div className="relative flex-1 w-full">
          <Search className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search documents by title, keyword, or description..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full rounded-2xl border border-slate-200 bg-slate-50/70 py-2.5 pl-10 pr-4 text-xs focus:border-nexora-500 focus:bg-white focus:outline-none focus:ring-1 focus:ring-nexora-500"
          />
        </div>
        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Filter className="h-4 w-4 text-slate-400 shrink-0" />
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full sm:w-auto rounded-2xl border border-slate-200 bg-slate-50/70 px-4 py-2.5 text-xs font-bold text-slate-700 focus:border-nexora-500 focus:outline-none"
          >
            <option value="All">All Categories</option>
            {DOCUMENT_CATEGORIES.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Responsive 3-Column Document Grid */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-20 text-slate-400 gap-3 os-card">
          <Loader2 className="h-8 w-8 animate-spin text-nexora-600" />
          <p className="text-xs font-semibold">Loading university documents...</p>
        </div>
      ) : filtered.length === 0 ? (
        <div className="os-card p-12 text-center">
          <p className="text-base font-bold text-slate-800">No documents match your query</p>
          <p className="mt-1 text-xs text-slate-500">Try adjusting your keyword filter or select 'All Categories'.</p>
        </div>
      ) : (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {filtered.map((doc) => (
            <DocumentCard key={doc.id} document={doc} />
          ))}
        </div>
      )}
    </div>
  );
}

