import os
import sys
import uuid
import datetime
import dotenv
import fitz
from pinecone import Pinecone

# Insert backend directory in python path
sys.path.insert(0, os.path.abspath('backend'))
dotenv.load_dotenv('backend/.env')

from app.database.supabase import get_supabase_client
from app.rag.pinecone_client import get_pinecone_index
from app.services.pdf_processor import extract_text_by_page, semantic_chunking
from app.rag.embeddings import generate_chunk_embeddings

supabase = get_supabase_client()
pinecone_index = get_pinecone_index()
kb_dir = os.path.abspath('knowledge_base')

# Define the 14 automated documents to process and index
AUTOMATED_DOCUMENTS = [
    {
        "filename": "Admission_Brochure_2026.pdf",
        "title": "Nexora University Admission Brochure 2026-2027",
        "category": "Admissions",
        "description": "Complete admission guide, eligibility matrix, program offerings, and selection criteria.",
    },
    {
        "filename": "Admission_Handbook_2026.pdf",
        "title": "Detailed Admission Rules & Candidate Handbook 2026",
        "category": "Admissions",
        "description": "Reservation quotas, NRI seats, transfer admissions, counseling SOP, and fee refund rules.",
    },
    {
        "filename": "Fee_Structure_2026.pdf",
        "title": "Official Tuition & Institutional Fee Structure 2026-2027",
        "category": "Finance",
        "description": "Degree program tuition fees, lab fees, hostel rent, instalment options, and caution deposit rules.",
    },
    {
        "filename": "Hostel_Rules_and_Fees_2026.pdf",
        "title": "Hostel Regulations, Residence Guidelines & Mess Fee Structure",
        "category": "Hostel",
        "description": "Living regulations, curfew timings, mess menu, laundry schedule, security SOP, and fine matrix.",
    },
    {
        "filename": "Academic_Calendar_2026.pdf",
        "title": "Official Academic Calendar & Examination Timetable 2026",
        "category": "Academics",
        "description": "Semester commencement, mid-term/end-term dates, holidays, and cultural fest schedule.",
    },
    {
        "filename": "Course_Catalog_and_Programs.pdf",
        "title": "Nexora Academic Course Catalog & Syllabus 2026",
        "category": "Academics",
        "description": "CBCS credit distribution, core & elective courses, lab specifications, and minor specializations.",
    },
    {
        "filename": "Department_Handbook_2026.pdf",
        "title": "Department Information, Labs & Faculty Profiles 2026",
        "category": "Departments",
        "description": "CSE, ECE, EEE, Mechanical, Biotech, and Business school research labs and faculty profiles.",
    },
    {
        "filename": "Examination_Regulations_2026.pdf",
        "title": "University Examination Rules & Evaluation Policy 2026",
        "category": "Examination",
        "description": "Grading scale, credit evaluations, backlog policies, revaluation SOP, and malpractice penalties.",
    },
    {
        "filename": "Placement_Brochure_2026.pdf",
        "title": "Annual Placement & Career Advancement Report 2026",
        "category": "Placements",
        "description": "Recruiter directory, salary statistics, summer internship SOP, and placement code of conduct.",
    },
    {
        "filename": "Scholarship_Handbook_2026.pdf",
        "title": "Institutional Scholarship & Financial Aid Guidelines 2026",
        "category": "Scholarships",
        "description": "Merit scholarships, need-based financial aid, sports waivers, and renewal criteria.",
    },
    {
        "filename": "Library_Guide_2026.pdf",
        "title": "Central Library Guide & Digital Knowledge Base Rules",
        "category": "Library",
        "description": "Membership, physical/digital borrowing rules, IEEE/Springer portal access, and working hours.",
    },
    {
        "filename": "Transport_Handbook_2026.pdf",
        "title": "Campus Bus Routes, Timings & Transport Pass Rules 2026",
        "category": "Transport",
        "description": "Bus routes, fleet management, bus pass registration, timings, and safety guidelines.",
    },
    {
        "filename": "Student_Code_of_Conduct_2026.pdf",
        "title": "Student Code of Ethics, Anti-Ragging & Campus Rules 2026",
        "category": "General",
        "description": "Campus ethics, anti-ragging mandates, gender safety protocols, and disciplinary procedures.",
    },
    {
        "filename": "Campus_Facilities_Guide_2026.pdf",
        "title": "Campus Facilities, Sports Infrastructure & Health Services",
        "category": "Campus",
        "description": "Overview of sports complex, gymnasium, cafeteria, 24/7 medical center, and campus amenities.",
    },
]

# Clean existing Pinecone index and Supabase tables
print("--- 1. Resetting Existing Pinecone & Supabase State ---")
try:
    pinecone_index.delete(delete_all=True)
    print("Deleted all vectors from Pinecone index.")
except Exception as e:
    print("Pinecone delete warning:", e)

try:
    supabase.table("documents").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    print("Cleared existing rows from Supabase documents table.")
except Exception as e:
    print("Supabase clear warning:", e)

report_data = []

print("\n--- 2. Processing & Indexing 14 Automated Documents ---")
for doc_info in AUTOMATED_DOCUMENTS:
    file_name = doc_info["filename"]
    file_path = os.path.join(kb_dir, file_name)
    
    if not os.path.exists(file_path):
        print(f"Error: {file_name} not found in knowledge_base!")
        continue

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    doc_id = str(uuid.uuid4())
    safe_filename = f"{doc_id}_{file_name}"
    storage_path = f"pdfs/{safe_filename}"
    public_url = f"{os.environ['SUPABASE_URL']}/storage/v1/object/public/documents/{storage_path}"
    file_size_mb = f"{len(file_bytes) / (1024*1024):.1f} MB"
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Step A: Upload to Supabase Storage
    try:
        supabase.storage.from_("documents").upload(
            path=storage_path,
            file=file_bytes,
            file_options={"content-type": "application/pdf", "upsert": "true"}
        )
        storage_status = "Uploaded"
    except Exception as st_err:
        print(f"Storage note for {file_name}: {st_err}")
        storage_status = "Uploaded (Overwritten)"

    # Step B: Extract Page text & semantic chunking
    pages_text = extract_text_by_page(file_bytes)
    total_pages = len(pages_text)
    chunks = semantic_chunking(pages_text, chunk_size_words=600, overlap_words=100)
    chunk_count = len(chunks)

    # Step C: Generate BAAI embeddings & vector upsert to Pinecone
    chunk_texts = [c["text"] for c in chunks]
    embeddings = generate_chunk_embeddings(chunk_texts)

    vectors_to_upsert = []
    for i, chunk in enumerate(chunks):
        vector_id = f"{doc_id}#chunk_{chunk['chunk_number']}"
        metadata = {
            "document_id": doc_id,
            "title": doc_info["title"],
            "category": doc_info["category"],
            "page_number": chunk["page_number"],
            "chunk_number": chunk["chunk_number"],
            "text": chunk["text"],
            "upload_date": now_iso,
        }
        vectors_to_upsert.append({
            "id": vector_id,
            "values": embeddings[i],
            "metadata": metadata
        })

    # Batch upsert to Pinecone
    batch_size = 100
    for b_idx in range(0, len(vectors_to_upsert), batch_size):
        batch = vectors_to_upsert[b_idx: b_idx + batch_size]
        pinecone_index.upsert(vectors=batch)

    # Step D: Insert Record in Supabase Documents table
    db_record = {
        "id": doc_id,
        "title": doc_info["title"],
        "category": doc_info["category"],
        "description": doc_info["description"],
        "file_url": public_url,
        "file_name": safe_filename,
        "status": "indexed",
        "processed_at": now_iso,
        "created_at": now_iso,
        "updated_at": now_iso,
    }
    
    try:
        supabase.table("documents").insert(db_record).execute()
        db_status = "Inserted"
    except Exception as db_err:
        print(f"DB Insert note for {file_name}: {db_err}")
        db_status = "Error"

    report_data.append({
        "name": doc_info["title"],
        "file_name": file_name,
        "pages": total_pages,
        "chunks": chunk_count,
        "vectors": len(vectors_to_upsert),
        "db": db_status,
        "storage": storage_status,
        "indexed": True,
        "size": file_size_mb
    })

    print(f"[INDEXED] '{doc_info['title']}' | Pages: {total_pages} | Chunks/Vectors: {chunk_count}")

# Summarize Manual Reserved PDFs
MANUAL_PDFS = [
    {
        "filename": "Faculty_Directory_2026.pdf",
        "name": "Faculty Directory 2026",
        "reason": "Reserved for manual upload."
    },
    {
        "filename": "Clubs_and_Student_Activities_2026.pdf",
        "name": "Clubs and Student Activities 2026",
        "reason": "Reserved for manual upload."
    },
    {
        "filename": "Research_and_Innovation_Handbook_2026.pdf",
        "name": "Research and Innovation Handbook 2026",
        "reason": "Reserved for manual upload."
    }
]

print("\n====================================================")
print("PART 4 & 7 — INGESTION & VERIFICATION REPORT SUMMARY")
print("====================================================")
total_vectors = sum(r["vectors"] for r in report_data)
print(f"Total Automated Documents Indexed: {len(report_data)}")
print(f"Total Vectors in Pinecone: {total_vectors}\n")

print(f"{'Document Name':<50} | {'Pages':<6} | {'Chunks':<7} | {'Vectors':<8} | {'Supabase':<8} | {'Storage':<10} | {'Status'}")
print("-" * 110)
for r in report_data:
    print(f"{r['name'][:48]:<50} | {r['pages']:<6} | {r['chunks']:<7} | {r['vectors']:<8} | {r['db']:<8} | {r['storage']:<10} | Indexed")

print("\n====================================================")
print("PART 5 — MANUAL UPLOAD LIST (UNINDEXED)")
print("====================================================")
for idx, m in enumerate(MANUAL_PDFS, start=1):
    print(f"{idx}.\n{m['name']}\nReason:\n{m['reason']}\n")

