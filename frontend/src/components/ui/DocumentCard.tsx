import { FileText, Eye, Download, CheckCircle2, Layers, HardDrive, Calendar } from "lucide-react";
import type { Document } from "@/lib/data";
import { downloadPdf } from "@/lib/pdfLinks";

const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

interface DocumentCardProps {
  document: Document;
}

export function DocumentCard({ document }: DocumentCardProps) {
  // Resolve the full URL — file_url from API is already absolute (http://localhost:8000/...)
  // For mock/local data that only has a filename, build the full URL
  let pdfUrl = document.fileUrl || "";
  if (!pdfUrl && document.file_name) {
    const bare = document.file_name.replace(/^[a-f0-9\-]+_/, "");
    pdfUrl = `${BACKEND}/knowledge_base/${bare}`;
  }
  if (pdfUrl && pdfUrl.startsWith("/knowledge_base/")) {
    pdfUrl = `${BACKEND}${pdfUrl}`;
  }
  if (!pdfUrl) pdfUrl = `${BACKEND}/knowledge_base/Admission_Handbook_2026.pdf`;

  const handleDownload = (e: React.MouseEvent) => {
    e.preventDefault();
    downloadPdf(pdfUrl, document.file_name || document.name + ".pdf");
  };

  return (
    <div className="os-card p-6 flex flex-col justify-between group">
      <div className="space-y-4">
        {/* Header & Category Badge */}
        <div className="flex items-start justify-between gap-3">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-nexora-50 to-blue-100 text-nexora-700 shadow-inner group-hover:scale-105 transition-transform">
            <FileText className="h-6 w-6" />
          </div>
          <div className="flex flex-col items-end gap-1">
            <span className="rounded-full bg-slate-100 px-3 py-1 text-[11px] font-bold text-slate-700">
              {document.category}
            </span>
            <span className="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full">
              <CheckCircle2 className="h-3 w-3 text-emerald-500" />
              {document.status || "indexed"}
            </span>
          </div>
        </div>

        {/* Title & Description */}
        <div>
          <h3 className="text-base font-extrabold text-slate-900 line-clamp-1 group-hover:text-nexora-700 transition">
            {document.name}
          </h3>
          <p className="mt-2 text-xs leading-relaxed text-slate-500 line-clamp-2">
            {document.description}
          </p>
        </div>

        {/* Metadata Badges */}
        <div className="grid grid-cols-3 gap-1 rounded-xl bg-slate-50 p-2.5 text-[11px] font-semibold text-slate-500 border border-slate-100">
          <div className="flex items-center justify-center gap-1">
            <Layers className="h-3.5 w-3.5 text-slate-400" />
            <span>{document.pages || 12} Pages</span>
          </div>
          <div className="flex items-center justify-center gap-1 border-x border-slate-200">
            <HardDrive className="h-3.5 w-3.5 text-slate-400" />
            <span>{document.size || "1.4 MB"}</span>
          </div>
          <div className="flex items-center justify-center gap-1">
            <Calendar className="h-3.5 w-3.5 text-slate-400" />
            <span>{document.updatedAt || "2026-07-01"}</span>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="mt-6 flex gap-2 pt-2">
        <a
          href={pdfUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="flex flex-1 items-center justify-center gap-1.5 rounded-xl border border-slate-200 bg-white py-2.5 text-xs font-bold text-slate-700 shadow-xs transition hover:bg-slate-50 hover:text-slate-900"
        >
          <Eye className="h-3.5 w-3.5" /> View PDF
        </a>
        <button
          onClick={handleDownload}
          className="flex flex-1 items-center justify-center gap-1.5 rounded-xl bg-nexora-700 py-2.5 text-xs font-bold text-white shadow-md transition hover:bg-nexora-800"
        >
          <Download className="h-3.5 w-3.5" /> Download PDF
        </button>
      </div>
    </div>
  );
}

