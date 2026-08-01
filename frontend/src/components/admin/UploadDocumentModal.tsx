"use client";

import { useState } from "react";
import { X, Upload, FileText, AlertCircle } from "lucide-react";
import { DOCUMENT_CATEGORIES } from "@/lib/constants";
import { getAdminToken } from "@/lib/api";

interface UploadDocumentModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export function UploadDocumentModal({ isOpen, onClose, onSuccess }: UploadDocumentModalProps) {
  const [title, setTitle] = useState("");
  const [category, setCategory] = useState<string>(DOCUMENT_CATEGORIES[0]);
  const [description, setDescription] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  if (!isOpen) return null;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setError("");
    const selected = e.target.files?.[0];
    if (!selected) {
      setFile(null);
      return;
    }

    if (!selected.name.toLowerCase().endsWith(".pdf")) {
      setError("Please select a valid PDF document (.pdf).");
      setFile(null);
      return;
    }

    if (selected.size > 50 * 1024 * 1024) {
      setError("File size exceeds maximum 50MB limit.");
      setFile(null);
      return;
    }

    setFile(selected);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!file) {
      setError("Please select a PDF document file to upload.");
      return;
    }

    setUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("title", title);
      formData.append("category", category);
      if (description) formData.append("description", description);

      const token = getAdminToken() || "dev-token-admin-session-xyz";
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

      const res = await fetch(`${API_BASE_URL}/documents/upload-pdf`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      const data = await res.json();

      if (res.ok && data.status === "success") {
        setTitle("");
        setDescription("");
        setFile(null);
        onSuccess();
        onClose();
      } else {
        setError(data.detail || data.message || "Failed to upload document.");
      }
    } catch (err: any) {
      setError(err?.message || "Network error. Failed to upload document.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-sm">
      <div className="w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div className="flex items-center gap-2 text-slate-900 font-bold text-lg">
            <Upload className="h-5 w-5 text-nexora-600" />
            Upload PDF Document
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-600"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {error && (
          <div className="mt-4 flex items-center gap-2 rounded-lg bg-rose-50 p-3 text-sm border border-rose-200 text-rose-700">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="mt-4 space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700">Document Title</label>
            <input
              type="text"
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Admission Handbook 2026"
              className="mt-1 w-full rounded-lg border border-slate-200 px-4 py-2 text-sm focus:border-nexora-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700">Category</label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="mt-1 w-full rounded-lg border border-slate-200 px-4 py-2 text-sm focus:border-nexora-500 focus:outline-none"
            >
              {DOCUMENT_CATEGORIES.map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700">Description (Optional)</label>
            <textarea
              rows={2}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Brief description of the document contents..."
              className="mt-1 w-full rounded-lg border border-slate-200 px-4 py-2 text-sm focus:border-nexora-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700">Select PDF File</label>
            <div className="mt-1 flex items-center justify-center rounded-xl border-2 border-dashed border-slate-200 p-6 text-center hover:border-nexora-400">
              <input
                type="file"
                accept=".pdf,application/pdf"
                onChange={handleFileChange}
                className="hidden"
                id="pdf-file-upload"
              />
              <label htmlFor="pdf-file-upload" className="cursor-pointer">
                <FileText className="mx-auto h-8 w-8 text-nexora-600" />
                <span className="mt-2 block text-sm font-medium text-slate-700">
                  {file ? file.name : "Click to choose PDF file"}
                </span>
                <span className="text-xs text-slate-400">PDF up to 50MB</span>
              </label>
            </div>
          </div>

          <div className="mt-6 flex justify-end gap-3 border-t border-slate-100 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={uploading}
              className="rounded-lg bg-nexora-700 px-5 py-2 text-sm font-medium text-white hover:bg-nexora-800 disabled:opacity-50"
            >
              {uploading ? "Uploading & Processing..." : "Upload & Ingest PDF"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
