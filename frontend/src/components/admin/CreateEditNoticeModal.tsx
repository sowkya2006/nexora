"use client";

import { useState, useEffect } from "react";
import { X, Bell, Calendar, Tag, FileText, CheckCircle2, AlertCircle } from "lucide-react";

export interface NoticeData {
  id?: string;
  title: string;
  description: string;
  category: "Academic" | "Examination" | "Events" | "Administration";
  priority: "Low" | "Medium" | "High";
  publish_date: string;
  expiry_date?: string;
  attachment_url?: string;
  status: "published" | "draft" | "archived";
}

interface CreateEditNoticeModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (notice: NoticeData, isEdit: boolean) => void;
  noticeToEdit?: NoticeData | null;
}

export function CreateEditNoticeModal({
  isOpen,
  onClose,
  onSuccess,
  noticeToEdit,
}: CreateEditNoticeModalProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState<NoticeData["category"]>("Academic");
  const [priority, setPriority] = useState<NoticeData["priority"]>("Medium");
  const [publishDate, setPublishDate] = useState("");
  const [expiryDate, setExpiryDate] = useState("");
  const [attachmentUrl, setAttachmentUrl] = useState("");
  const [status, setStatus] = useState<NoticeData["status"]>("published");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (noticeToEdit) {
      setTitle(noticeToEdit.title || "");
      setDescription(noticeToEdit.description || "");
      setCategory(noticeToEdit.category || "Academic");
      setPriority(noticeToEdit.priority || "Medium");
      setPublishDate(noticeToEdit.publish_date || new Date().toISOString().split("T")[0]);
      setExpiryDate(noticeToEdit.expiry_date || "");
      setAttachmentUrl(noticeToEdit.attachment_url || "");
      setStatus(noticeToEdit.status || "published");
    } else {
      setTitle("");
      setDescription("");
      setCategory("Academic");
      setPriority("Medium");
      setPublishDate(new Date().toISOString().split("T")[0]);
      setExpiryDate("");
      setAttachmentUrl("");
      setStatus("published");
    }
    setError("");
  }, [noticeToEdit, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !description.trim()) {
      setError("Please fill in all required fields.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const noticePayload: NoticeData = {
        id: noticeToEdit?.id || `notice-${Date.now()}`,
        title: title.trim(),
        description: description.trim(),
        category,
        priority,
        publish_date: publishDate || new Date().toISOString().split("T")[0],
        expiry_date: expiryDate || undefined,
        attachment_url: attachmentUrl.trim() || undefined,
        status,
      };

      onSuccess(noticePayload, !!noticeToEdit);
      onClose();
    } catch (err: any) {
      setError(err?.message || "Failed to save notice.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 p-4 backdrop-blur-sm animate-fade-in">
      <div className="w-full max-w-xl rounded-2xl bg-white shadow-2xl overflow-hidden border border-slate-100">
        <div className="flex items-center justify-between border-b border-slate-200 bg-slate-50 px-6 py-4">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-nexora-100 text-nexora-700">
              <Bell className="h-4 w-4" />
            </div>
            <h2 className="text-lg font-bold text-slate-900">
              {noticeToEdit ? "Edit Announcement Notice" : "Create New Notice"}
            </h2>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-200 hover:text-slate-700 transition"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {error && (
          <div className="mx-6 mt-4 flex items-center gap-2 rounded-lg bg-rose-50 p-3 text-xs font-medium text-rose-700 border border-rose-200">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="p-6 space-y-4 max-h-[80vh] overflow-y-auto">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">Notice Title *</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. End-Semester Examination Schedule July 2026"
              className="mt-1 w-full rounded-xl border border-slate-200 px-4 py-2.5 text-sm focus:border-nexora-500 focus:outline-none focus:ring-1 focus:ring-nexora-500"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">Description *</label>
            <textarea
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Detailed announcement description..."
              className="mt-1 w-full rounded-xl border border-slate-200 px-4 py-2.5 text-sm focus:border-nexora-500 focus:outline-none focus:ring-1 focus:ring-nexora-500"
              required
            />
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">Category</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value as any)}
                className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2.5 text-sm focus:border-nexora-500 focus:outline-none"
              >
                <option value="Academic">Academic</option>
                <option value="Examination">Examination</option>
                <option value="Events">Events</option>
                <option value="Administration">Administration</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">Priority</label>
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value as any)}
                className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2.5 text-sm focus:border-nexora-500 focus:outline-none"
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High Priority</option>
              </select>
            </div>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">Publish Date</label>
              <input
                type="date"
                value={publishDate}
                onChange={(e) => setPublishDate(e.target.value)}
                className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2.5 text-sm focus:border-nexora-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">Status</label>
              <select
                value={status}
                onChange={(e) => setStatus(e.target.value as any)}
                className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2.5 text-sm focus:border-nexora-500 focus:outline-none"
              >
                <option value="published">Published</option>
                <option value="draft">Draft</option>
                <option value="archived">Archived</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">Attachment PDF URL (Optional)</label>
            <input
              type="text"
              value={attachmentUrl}
              onChange={(e) => setAttachmentUrl(e.target.value)}
              placeholder="e.g. /knowledge_base/Academic_Calendar_2026.pdf"
              className="mt-1 w-full rounded-xl border border-slate-200 px-4 py-2.5 text-sm focus:border-nexora-500 focus:outline-none"
            />
          </div>

          <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={onClose}
              className="rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-50 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="rounded-xl bg-nexora-700 px-5 py-2.5 text-sm font-semibold text-white hover:bg-nexora-800 transition shadow-md disabled:opacity-50"
            >
              {loading ? "Saving..." : noticeToEdit ? "Update Notice" : "Publish Notice"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
