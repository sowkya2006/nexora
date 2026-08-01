export interface ChatSource {
  document_name: string;
  page?: number;
  snippet?: string;
  document_id?: string;
  file_name?: string;
  download_url?: string;
  view_url?: string;
}

export interface ChatResponse {
  answer: string;
  sources: ChatSource[];
  confidence_score?: number;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  sources?: ChatSource[];
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
// Backend static file server — knowledge_base PDFs are served here
const KB_BASE = "http://localhost:8000/knowledge_base";

/**
 * Map document names to their exact knowledge_base filenames.
 * The backend RAG returns document_name from Pinecone metadata.
 * We need to resolve that to the actual PDF filename.
 */
const DOC_NAME_TO_FILE: Record<string, string> = {
  "Admission Handbook 2026":               "Admission_Handbook_2026.pdf",
  "Fee Structure 2026":                    "Fee_Structure_2026.pdf",
  "Fee Structure 2026-27":                 "Fee_Structure_2026.pdf",
  "Hostel & Accommodation Guide":          "Hostel_Accommodation_Guide.pdf",
  "Hostel Accommodation Guide":            "Hostel_Accommodation_Guide.pdf",
  "Placement Report 2026":                 "Placement_Report_2026.pdf",
  "Academic Regulations 2026":             "Academic_Regulations_2026.pdf",
  "Scholarships & Financial Aid 2026":     "Scholarships_Financial_Aid_2026.pdf",
  "Scholarships Financial Aid 2026":       "Scholarships_Financial_Aid_2026.pdf",
  "Course Catalog & Programmes":           "Course_Catalog_and_Programs.pdf",
  "Course Catalog and Programs":           "Course_Catalog_and_Programs.pdf",
  "Academic Calendar 2026-27":             "Academic_Calendar_2026.pdf",
  "Academic Calendar 2026":               "Academic_Calendar_2026.pdf",
  "Library Guide 2026":                    "Library_Guide_2026.pdf",
  "Transport Guide 2026":                  "Transport_Guide_2026.pdf",
  "Research & Innovation Handbook":        "Research_Innovation_Handbook.pdf",
  "Research Innovation Handbook":          "Research_Innovation_Handbook.pdf",
  "Department Handbook: CSE":              "Department_Handbook_CSE.pdf",
  "Department Handbook CSE":               "Department_Handbook_CSE.pdf",
  "Student Handbook & Code of Conduct":    "Student_Handbook_Code_of_Conduct.pdf",
  "Student Handbook Code of Conduct":      "Student_Handbook_Code_of_Conduct.pdf",
  "Campus Facilities Guide":               "Campus_Facilities_Guide.pdf",
  "International Exchange Programme":      "International_Exchange_Programme.pdf",
  "Industry Interface & MoU Directory":    "Industry_Interface_MoU_Directory.pdf",
  "NSS, NCC & Social Outreach Handbook":   "NSS_NCC_Social_Outreach.pdf",
  // Legacy filenames from older phases
  "Admission_Brochure_2026":               "Admission_Handbook_2026.pdf",
  "Hostel_Rules_and_Fees_2026":            "Hostel_Accommodation_Guide.pdf",
  "Placement_Brochure_2026":               "Placement_Report_2026.pdf",
  "Department_Handbook_2026":              "Department_Handbook_CSE.pdf",
  "Student_Code_of_Conduct_2026":          "Student_Handbook_Code_of_Conduct.pdf",
};

/**
 * Resolve a document name or file_name from the RAG response
 * to a full URL pointing at the backend static file server.
 */
function resolvePdfUrl(source: any): string {
  // 1. If backend already gave a full file_url, use it
  if (source.file_url && source.file_url.startsWith("http")) {
    return source.file_url;
  }
  // 2. If there's a file_name field, serve directly
  if (source.file_name) {
    const clean = source.file_name.replace(/^.*[\\/]/, ""); // basename only
    return `${KB_BASE}/${clean}`;
  }
  // 3. Map document_name via lookup table
  const docName: string = source.document || source.document_name || "";
  if (docName && DOC_NAME_TO_FILE[docName]) {
    return `${KB_BASE}/${DOC_NAME_TO_FILE[docName]}`;
  }
  // 4. Fuzzy match: try replacing spaces with underscores + .pdf
  if (docName) {
    const guessed = docName.replace(/\s+/g, "_").replace(/[^a-zA-Z0-9_\-.]/g, "") + ".pdf";
    return `${KB_BASE}/${guessed}`;
  }
  return `${KB_BASE}/Admission_Handbook_2026.pdf`;
}

/**
 * Send real user query to RAG Chat API (/api/v1/chat/query)
 */
export async function sendChatMessage(
  message: string,
  sessionId: string,
  history: ChatMessage[] = []
): Promise<ChatResponse> {
  try {
    const res = await fetch(`${API_BASE_URL}/chat/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: message,
        session_id: sessionId,
        history: history.map((m) => ({ role: m.role, content: m.content })),
      }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "UniSphere AI returned an error.");
    }

    const data = await res.json();

    const sources: ChatSource[] = (data.sources || []).map((s: any) => {
      const pdfUrl = resolvePdfUrl(s);
      return {
        document_name: s.document || s.document_name || "University Document",
        page: s.page || 1,
        snippet: s.snippet || "",
        document_id: s.document_id,
        file_name: s.file_name,
        view_url: pdfUrl,
        download_url: pdfUrl,
      };
    });

    return {
      answer: data.answer || "I could not find this information in the uploaded university documents.",
      sources,
      confidence_score: data.confidence_score,
    };
  } catch (err: any) {
    console.error("Chat API error:", err);
    return {
      answer: "I could not find this information in the uploaded university documents.",
      sources: [],
      confidence_score: 0.0,
    };
  }
}
