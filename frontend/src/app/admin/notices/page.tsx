"use client";

import { useState, useEffect, useRef } from "react";
import {
  Plus, Pencil, Trash2, Bell, Search, Filter,
  CheckCircle2, Tag, Calendar, RefreshCw, Loader2,
} from "lucide-react";
import { CreateEditNoticeModal, NoticeData } from "@/components/admin/CreateEditNoticeModal";
import { fetchWithAuth } from "@/lib/api";

type ToastType = "success" | "error";

export default function AdminNoticesPage() {
  const [noticesList, setNoticesList] = useState<NoticeData[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [noticeToEdit, setNoticeToEdit] = useState<NoticeData | null>(null);
  const [toast, setToast] = useState<{ type: ToastType; msg: string } | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const toastTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const showToast = (type: ToastType, msg: string) => {
    setToast({ type, msg });
    if (toastTimer.current) clearTimeout(toastTimer.current);
    toastTimer.current = setTimeout(() => setToast(null), 3500);
  };

  const loadNotices = async () => {
    setLoading(true);
    try {
      const data = await fetchWithAuth("/notices/");
      if (data?.notices) {
        setNoticesList(
          data.notices.map((n: any) => ({
            id: n.id,
            title: n.title,
            description: n.description || "",
            category: n.category || "Academic",
            priority: n.priority || "Medium",
            publish_date: n.published_at ? n.published_at.split("T")[0] : (n.created_at ? n.created_at.split("T")[0] : ""),
            expiry_date: n.expiry_date || "",
            attachment_url: n.attachment_url || "",
            status: n.status || "published",
          }))
        );
      }
    } catch {
      showToast("error", "Failed to load notices.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadNotices(); }, []);

  const handleCreateOrUpdate = async (notice: NoticeData, isEdit: boolean) => {
    const payload = {
      title: notice.title,
      description: notice.description,
      category: notice.category,
      attachment_url: notice.attachment_url || null,
      status: notice.status,
    };

    if (isEdit && notice.id) {
      setNoticesList((prev) => prev.map((n) => (n.id === notice.id ? notice : n)));
      try {
        const res = await fetchWithAuth(`/notices/${notice.id}`, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
        if (res?.status !== "success") throw new Error();
        showToast("success", "Notice updated successfully.");
      } catch {
        showToast("error", "Failed to update notice.");
        loadNotices();
      }
    } else {
      try {
        const res = await fetchWithAuth("/notices/", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        if (res?.status === "success" && res.data) {
          setNoticesList((prev) => [{ ...notice, id: res.data.id || notice.id }, ...prev]);
          showToast("success", "Notice published successfully.");
        } else {
          throw new Error();
        }
      } catch {
        showToast("error", "Failed to create notice.");
      }
    }
  };

  const handleDelete = async (id?: string) => {
    if (!id) return;
    if (!confirm("Delete this notice? This cannot be undone.")) return;
    setDeletingId(id);
    try {
      await fetchWithAuth(`/notices/${id}`, { method: "DELETE" });
      setNoticesList((prev) => prev.filter((n) => n.id !== id));
      showToast("success", "Notice deleted.");
    } catch {
      showToast("error", "Failed to delete notice.");
    } finally {
      setDeletingId(null);
    }
  };

  const handleTogglePublish = async (notice: NoticeData) => {
    const newStatus: NoticeData["status"] = notice.status === "published" ? "draft" : "published";
    const updated = { ...notice, status: newStatus };
    setNoticesList((prev) => prev.map((n) => (n.id === notice.id ? updated : n)));
    try {
      await fetchWithAuth(`/notices/${notice.id}`, {
        method: "PUT",
        body: JSON.stringify({ status: newStatus }),
      });
      showToast("success", `Notice ${newStatus === "published" ? "published" : "set to draft"}.`);
    } catch {
      showToast("error", "Failed to update status.");
      loadNotices();
    }
  };

  const filtered = noticesList.filter((n) => {
    const q = searchQuery.toLowerCase();
    const matchSearch = n.title.toLowerCase().includes(q) || n.description.toLowerCase().includes(q);
    const matchCat = selectedCategory === "All" || n.category === selectedCategory;
    return matchSearch && matchCat;
  });

  const priorityBadge = (p: string) => {
    if (p === "High") return "bg-rose-50 text-rose-700 border-rose-200";
    if (p === "Low") return "bg-slate-100 text-slate-600 border-slate-200";
    return "bg-amber-50 text-amber-700 border-amber-200";
  };

  return (
    <div className="p-8 space-y-6 animate-fade-in">
      {toast && (
        <div className={`fixed top-6 right-6 z-50 flex items-center gap-2 rounded-xl px-5 py-3 text-sm font-semibold text-white shadow-2xl animate-fade-in ${toast.type === "success" ? "bg-emerald-600" : "bg-rose-600"}`}>
          <CheckCircle2 className="h-4 w-4 shrink-0" /> {toast.msg}
        </div>
      )}

      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Notices Management</h1>
          <p className="mt-1 text-slate-500 text-sm">Create, edit, and publish official announcements</p>
        </div>
        <div className="flex items-center gap-3">
          <button onClick={loadNotices} className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm font-medium hover:bg-slate-50 transition">
            <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} />
          </button>
          <button
            onClick={() => { setNoticeToEdit(null); setIsModalOpen(true); }}
            className="inline-flex items-center gap-2 rounded-xl bg-nexora-700 px-4 py-2.5 text-sm font-semibold text-white hover:bg-nexora-800 transition shadow-md"
          >
            <Plus className="h-4 w-4" /> Create Notice
          </button>
        </div>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <input type="text" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search notices by title or content..."
            className="w-full rounded-xl border border-slate-200 py-2.5 pl-10 pr-4 text-sm focus:border-nexora-500 focus:outline-none" />
        </div>
        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-slate-400" />
          <select value={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)}
            className="rounded-xl border border-slate-200 px-3 py-2.5 text-sm bg-white focus:outline-none">
            {["All", "Academic", "Examination", "Events", "Administration"].map((c) => (
              <option key={c} value={c}>{c === "All" ? "All Categories" : c}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="space-y-3">
        {loading ? (
          <div className="os-card p-8 text-center text-slate-400">
            <Loader2 className="h-6 w-6 animate-spin mx-auto mb-2" /> Loading notices...
          </div>
        ) : filtered.length === 0 ? (
          <div className="os-card p-10 text-center">
            <Bell className="h-10 w-10 text-slate-200 mx-auto mb-3" />
            <p className="font-semibold text-slate-700">No notices found</p>
            <p className="text-xs text-slate-400 mt-1">Create your first notice using the button above.</p>
          </div>
        ) : (
          filtered.map((notice) => (
            <div key={notice.id} className="os-card p-5 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div className="space-y-1.5 flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="inline-flex items-center gap-1 rounded-full bg-nexora-50 px-2.5 py-0.5 text-xs font-semibold text-nexora-700">
                    <Tag className="h-3 w-3" /> {notice.category}
                  </span>
                  {notice.priority && (
                    <span className={`rounded-full px-2.5 py-0.5 text-[10px] font-bold border ${priorityBadge(notice.priority)}`}>
                      {notice.priority} Priority
                    </span>
                  )}
                  {notice.publish_date && (
                    <span className="text-xs text-slate-400 flex items-center gap-1">
                      <Calendar className="h-3 w-3" /> {notice.publish_date}
                    </span>
                  )}
                </div>
                <h3 className="font-bold text-slate-900 truncate">{notice.title}</h3>
                <p className="text-xs text-slate-500 line-clamp-2">{notice.description}</p>
              </div>

              <div className="flex items-center gap-2 shrink-0">
                <button
                  onClick={() => handleTogglePublish(notice)}
                  className={`rounded-full px-3 py-1.5 text-xs font-semibold border transition ${
                    notice.status === "published"
                      ? "bg-emerald-50 text-emerald-700 border-emerald-200 hover:bg-emerald-100"
                      : "bg-slate-100 text-slate-600 border-slate-200 hover:bg-slate-200"
                  }`}
                >
                  {notice.status === "published" ? "Published" : "Draft"}
                </button>
                <button onClick={() => { setNoticeToEdit(notice); setIsModalOpen(true); }}
                  className="rounded-lg p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-700 transition" title="Edit">
                  <Pencil className="h-4 w-4" />
                </button>
                <button onClick={() => handleDelete(notice.id)} disabled={deletingId === notice.id}
                  className="rounded-lg p-2 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition disabled:opacity-50" title="Delete">
                  {deletingId === notice.id ? <Loader2 className="h-4 w-4 animate-spin" /> : <Trash2 className="h-4 w-4" />}
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      <CreateEditNoticeModal
        isOpen={isModalOpen}
        onClose={() => { setIsModalOpen(false); setNoticeToEdit(null); }}
        onSuccess={handleCreateOrUpdate}
        noticeToEdit={noticeToEdit}
      />
    </div>
  );
}
