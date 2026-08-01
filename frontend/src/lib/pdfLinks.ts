/**
 * Central PDF URL resolver.
 * All PDFs are served from the FastAPI backend static mount:
 *   http://localhost:8000/knowledge_base/<filename>
 *
 * Use pdfUrl(filename) everywhere instead of hardcoding paths.
 */
const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
const KB = `${BACKEND}/knowledge_base`;

export const PDF = {
  // Admissions
  admissionHandbook:     `${KB}/Admission_Handbook_2026.pdf`,
  // Finance
  feeStructure:          `${KB}/Fee_Structure_2026.pdf`,
  // Hostel
  hostelGuide:           `${KB}/Hostel_Accommodation_Guide.pdf`,
  // Placements
  placementReport:       `${KB}/Placement_Report_2026.pdf`,
  // Academics
  academicRegulations:   `${KB}/Academic_Regulations_2026.pdf`,
  academicCalendar:      `${KB}/Academic_Calendar_2026.pdf`,
  courseCatalog:         `${KB}/Course_Catalog_and_Programs.pdf`,
  // Scholarships
  scholarships:          `${KB}/Scholarships_Financial_Aid_2026.pdf`,
  // Library
  libraryGuide:          `${KB}/Library_Guide_2026.pdf`,
  // Transport
  transportGuide:        `${KB}/Transport_Guide_2026.pdf`,
  // Research
  researchHandbook:      `${KB}/Research_Innovation_Handbook.pdf`,
  // Departments
  departmentCSE:         `${KB}/Department_Handbook_CSE.pdf`,
  // Student life
  studentHandbook:       `${KB}/Student_Handbook_Code_of_Conduct.pdf`,
  campusFacilities:      `${KB}/Campus_Facilities_Guide.pdf`,
  // Reserved
  international:         `${KB}/International_Exchange_Programme.pdf`,
  industryMoU:           `${KB}/Industry_Interface_MoU_Directory.pdf`,
  nssNcc:                `${KB}/NSS_NCC_Social_Outreach.pdf`,
};

/** Generic resolver — pass any filename */
export function pdfUrl(filename: string): string {
  return `${KB}/${filename}`;
}

/** Programmatic download trigger */
export function downloadPdf(url: string, filename?: string) {
  const a = document.createElement("a");
  a.href = url;
  a.download = filename || url.split("/").pop() || "document.pdf";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}
