"use client";

import { X, FileText, Layers, Clock, ShieldCheck, Database, HardDrive, User, RefreshCw } from "lucide-react";
import { DocumentItem } from "@/components/admin/AdminDocumentRow";

interface DocumentMetadataModalProps {
  isOpen: boolean;
  onClose: () => void;
  document: DocumentItem | null;
  onReprocess?: (id: string) => void;
}

export function DocumentMetadataModal({
  isOpen,
  onClose,
  document,
  onReprocess,
}: DocumentMetadataModalProps) {
  if (!isOpen || !document) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 p-4 backdrop-blur-sm animate-fade-in">
      <div className="w-full max-w-md rounded-2xl bg-white shadow-2xl overflow-hidden border border-slate-100">
        <div className="flex items-center justify-between border-b border-slate-200 bg-slate-50 px-6 py-4">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-nexora-100 text-nexora-700">
              <FileText className="h-4 w-4" />
            </div>
            <h2 className="text-base font-bold text-slate-900">Document Metadata</h2>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-200 hover:text-slate-700 transition"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="p-6 space-y-4 text-xs text-slate-600">
          <div>
            <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Document Title</p>
            <p className="text-sm font-bold text-slate-900 mt-0.5">{document.title}</p>
          </div>

          <div className="grid grid-cols-2 gap-3 pt-2">
            <div className="rounded-xl bg-slate-50 p-3 border border-slate-100">
              <p className="text-[10px] text-slate-400 font-semibold uppercase">Category</p>
              <p className="font-bold text-slate-800 mt-0.5">{document.category}</p>
            </div>

            <div className="rounded-xl bg-slate-50 p-3 border border-slate-100">
              <p className="text-[10px] text-slate-400 font-semibold uppercase">Status</p>
              <p className="font-bold text-nexora-700 mt-0.5 capitalize">{document.status}</p>
            </div>

            <div className="rounded-xl bg-slate-50 p-3 border border-slate-100">
              <p className="text-[10px] text-slate-400 font-semibold uppercase flex items-center gap-1">
                <Layers className="h-3 w-3 text-nexora-600" /> Vector Chunks
              </p>
              <p className="font-bold text-slate-800 mt-0.5">{document.chunk_count || 0} Indexed</p>
            </div>

            <div className="rounded-xl bg-slate-50 p-3 border border-slate-100">
              <p className="text-[10px] text-slate-400 font-semibold uppercase flex items-center gap-1">
                <Database className="h-3 w-3 text-emerald-600" /> Vector Index
              </p>
              <p className="font-bold text-slate-800 mt-0.5">nexora-university</p>
            </div>
          </div>

          <div className="space-y-2 pt-2 border-t border-slate-100">
            <p className="flex items-center justify-between">
              <span className="text-slate-500">Document ID:</span>
              <span className="font-mono text-[11px] text-slate-800">{document.id}</span>
            </p>
            {document.created_at && (
              <p className="flex items-center justify-between">
                <span className="text-slate-500">Upload Date:</span>
                <span className="font-medium text-slate-800">{new Date(document.created_at).toLocaleDateString()}</span>
              </p>
            )}
            <p className="flex items-center justify-between">
              <span className="text-slate-500">Embedding Model:</span>
              <span className="font-medium text-slate-800">BAAI/bge-large-en-v1.5</span>
            </p>
            <p className="flex items-center justify-between">
              <span className="text-slate-500">Embedding Dimensions:</span>
              <span className="font-medium text-slate-800">1024-dim</span>
            </p>
          </div>

          <div className="flex items-center justify-between pt-4 border-t border-slate-100">
            {document.file_url ? (
              <a
                href={document.file_url}
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition"
              >
                Preview PDF
              </a>
            ) : <div />}

            {onReprocess && (
              <button
                onClick={() => {
                  onReprocess(document.id);
                  onClose();
                }}
                className="inline-flex items-center gap-1.5 rounded-xl bg-nexora-700 px-4 py-2 text-xs font-semibold text-white hover:bg-nexora-800 transition"
              >
                <RefreshCw className="h-3.5 w-3.5" /> Reprocess Document
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
