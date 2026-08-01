"use client";

import { FileText, Layers, CheckCircle2, Clock, AlertTriangle, Loader2 } from "lucide-react";

export interface DocumentItem {
  id: string;
  title: string;
  category: string;
  status: "uploaded" | "processing" | "indexed" | "failed" | string;
  chunk_count?: number;
  file_url?: string;
  created_at?: string;
  updated_at?: string;
}

interface AdminDocumentRowProps {
  document: DocumentItem;
  onDelete?: (id: string) => void;
  onViewMetadata?: (document: DocumentItem) => void;
}

export function AdminDocumentRow({ document, onDelete, onViewMetadata }: AdminDocumentRowProps) {
  const getStatusBadge = () => {
    switch (document.status) {
      case "indexed":
      case "published":
        return (
          <span className="inline-flex items-center gap-1 rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-semibold text-emerald-700 border border-emerald-200">
            <CheckCircle2 className="h-3 w-3" /> Indexed
          </span>
        );
      case "processing":
        return (
          <span className="inline-flex items-center gap-1 rounded-full bg-amber-50 px-2.5 py-1 text-xs font-semibold text-amber-700 border border-amber-200">
            <Loader2 className="h-3 w-3 animate-spin" /> Processing
          </span>
        );
      case "failed":
        return (
          <span className="inline-flex items-center gap-1 rounded-full bg-rose-50 px-2.5 py-1 text-xs font-semibold text-rose-700 border border-rose-200">
            <AlertTriangle className="h-3 w-3" /> Failed
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 rounded-full bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600 border border-slate-200">
            <Clock className="h-3 w-3" /> Uploaded
          </span>
        );
    }
  };

  return (
    <div className="flex flex-col gap-4 rounded-xl border border-slate-200 bg-white p-5 sm:flex-row sm:items-center sm:justify-between shadow-sm hover:shadow transition">
      <div className="flex items-start gap-3">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-nexora-50 text-nexora-600">
          <FileText className="h-5 w-5" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h3 className="font-semibold text-slate-900">{document.title}</h3>
            {getStatusBadge()}
          </div>
          <p className="mt-1 text-xs text-slate-500 flex items-center gap-3">
            <span>{document.category}</span>
            {document.chunk_count !== undefined && document.chunk_count > 0 && (
              <span className="flex items-center gap-1 text-nexora-700 font-medium">
                <Layers className="h-3 w-3" /> {document.chunk_count} Chunks Indexed
              </span>
            )}
          </p>
        </div>
      </div>
      <div className="flex flex-wrap items-center gap-2">
        {onViewMetadata && (
          <button
            onClick={() => onViewMetadata(document)}
            className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50 transition"
          >
            Metadata
          </button>
        )}
        {document.file_url && (
          <a
            href={document.file_url}
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-lg border border-nexora-200 bg-nexora-50 px-3 py-1.5 text-xs font-medium text-nexora-700 hover:bg-nexora-100 transition"
          >
            View PDF
          </a>
        )}
        <button
          onClick={() => onDelete && onDelete(document.id)}
          className="rounded-lg border border-rose-200 px-3 py-1.5 text-xs font-medium text-rose-600 hover:bg-rose-50 transition"
        >
          Delete
        </button>
      </div>
    </div>
  );
}
