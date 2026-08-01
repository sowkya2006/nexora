import sys
import os
import uuid
import datetime
import dotenv

sys.path.insert(0, os.path.abspath('backend'))
dotenv.load_dotenv('backend/.env')

from app.database.supabase import get_supabase_client
from app.rag.pinecone_client import get_pinecone_index
from app.services.pdf_processor import extract_text_by_page, semantic_chunking
from app.rag.embeddings import generate_chunk_embeddings

supabase = get_supabase_client()
pinecone_index = get_pinecone_index()
kb_dir = os.path.abspath('knowledge_base')

docs = [
    ("Admission_Brochure_2026.pdf", "Nexora University Admission Brochure 2026-2027", "Admissions", "Complete admission guide, eligibility matrix, program offerings, and selection criteria."),
    ("Admission_Handbook_2026.pdf", "Detailed Admission Rules & Candidate Handbook 2026", "Admissions", "Reservation quotas, NRI seats, transfer admissions, counseling SOP, and fee refund rules."),
    ("Fee_Structure_2026.pdf", "Official Tuition & Institutional Fee Structure 2026-2027", "Finance", "Degree program tuition fees, lab fees, hostel rent, instalment options, and caution deposit rules."),
    ("Hostel_Rules_and_Fees_2026.pdf", "Hostel Regulations, Residence Guidelines & Mess Fee Structure", "Hostel", "Living regulations, curfew timings, mess menu, laundry schedule, security SOP, and fine matrix."),
    ("Academic_Calendar_2026.pdf", "Official Academic Calendar & Examination Timetable 2026", "Academics", "Semester commencement, mid-term/end-term dates, holidays, and cultural fest schedule."),
    ("Course_Catalog_and_Programs.pdf", "Nexora Academic Course Catalog & Syllabus 2026", "Academics", "CBCS credit distribution, core & elective courses, lab specifications, and minor specializations."),
    ("Department_Handbook_2026.pdf", "Department Information, Labs & Faculty Profiles 2026", "Departments", "CSE, ECE, EEE, Mechanical, Biotech, and Business school research labs and faculty profiles."),
    ("Examination_Regulations_2026.pdf", "University Examination Rules & Evaluation Policy 2026", "Examination", "Grading scale, credit evaluations, backlog policies, revaluation SOP, and malpractice penalties."),
    ("Placement_Brochure_2026.pdf", "Annual Placement & Career Advancement Report 2026", "Placements", "Recruiter directory, salary statistics, summer internship SOP, and placement code of conduct."),
    ("Scholarship_Handbook_2026.pdf", "Institutional Scholarship & Financial Aid Guidelines 2026", "Scholarships", "Merit scholarships, need-based financial aid, sports waivers, and renewal criteria."),
    ("Library_Guide_2026.pdf", "Central Library Guide & Digital Knowledge Base Rules", "Library", "Membership, physical/digital borrowing rules, IEEE/Springer portal access, and working hours."),
    ("Transport_Handbook_2026.pdf", "Campus Bus Routes, Timings & Transport Pass Rules 2026", "Transport", "Bus routes, fleet management, bus pass registration, timings, and safety guidelines."),
    ("Student_Code_of_Conduct_2026.pdf", "Student Code of Ethics, Anti-Ragging & Campus Rules 2026", "General", "Campus ethics, anti-ragging mandates, gender safety protocols, and disciplinary procedures."),
    ("Campus_Facilities_Guide_2026.pdf", "Campus Facilities, Sports Infrastructure & Health Services", "Campus", "Overview of sports complex, gymnasium, cafeteria, 24/7 medical center, and campus amenities.")
]

print("--- Resetting Pinecone & Supabase State ---")
try:
    pinecone_index.delete(delete_all=True)
    print("Cleared Pinecone vectors.")
except Exception as e:
    print("Pinecone clear warning:", e)

try:
    supabase.table("documents").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    print("Cleared Supabase documents table.")
except Exception as e:
    print("Supabase clear warning:", e)

report_data = []

print("\n--- Ingesting 14 Multi-Page Documents ---")
for fname, title, cat, desc in docs:
    fpath = os.path.join(kb_dir, fname)
    if not os.path.exists(fpath):
        print(f"Error: {fname} missing")
        continue

    with open(fpath, "rb") as f:
        fbytes = f.read()

    doc_id = str(uuid.uuid4())
    safe_fname = f"{doc_id}_{fname}"
    st_path = f"pdfs/{safe_fname}"
    pub_url = f"{os.environ['SUPABASE_URL']}/storage/v1/object/public/documents/{st_path}"
    file_size_mb = f"{len(fbytes) / (1024*1024):.1f} MB"
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

    try:
        supabase.storage.from_("documents").upload(
            path=st_path,
            file=fbytes,
            file_options={"content-type": "application/pdf", "upsert": "true"}
        )
        st_status = "Uploaded"
    except Exception:
        st_status = "Uploaded (Exist)"

    pages_text = extract_text_by_page(fbytes)
    total_pages = len(pages_text)
    chunks = semantic_chunking(pages_text, chunk_size_words=600, overlap_words=100)
    chunk_count = len(chunks)

    chunk_texts = [c["text"] for c in chunks]
    embeddings = generate_chunk_embeddings(chunk_texts)

    vecs = []
    for i, c in enumerate(chunks):
        vecs.append({
            "id": f"{doc_id}#chunk_{c['chunk_number']}",
            "values": embeddings[i],
            "metadata": {
                "document_id": doc_id,
                "title": title,
                "category": cat,
                "page_number": c["page_number"],
                "chunk_number": c["chunk_number"],
                "text": c["text"],
                "upload_date": now_iso
            }
        })

    if vecs:
        batch_size = 100
        for b_idx in range(0, len(vecs), batch_size):
            pinecone_index.upsert(vectors=vecs[b_idx:b_idx+batch_size])

    db_rec = {
        "id": doc_id,
        "title": title,
        "category": cat,
        "description": desc,
        "file_url": pub_url,
        "file_name": safe_fname,
        "status": "indexed"
    }
    supabase.table("documents").insert(db_rec).execute()

    report_data.append({
        "name": title,
        "file_name": fname,
        "pages": total_pages,
        "chunks": chunk_count,
        "vectors": len(vecs),
        "db": "Inserted",
        "storage": st_status,
        "size": file_size_mb
    })
    print(f"[INDEXED] {title[:40]:<40} | Pages: {total_pages:<2} | Chunks/Vectors: {chunk_count}")

print("\n====================================================")
print("FINAL INGESTION SUMMARY REPORT")
print("====================================================")
total_vecs = sum(r["vectors"] for r in report_data)
print(f"Total Automated Documents Indexed: {len(report_data)}")
print(f"Total Vectors in Pinecone: {total_vecs}\n")

print(f"{'Document Name':<45} | {'Pages':<5} | {'Chunks':<6} | {'Vectors':<7} | {'Supabase':<8} | {'Storage':<8}")
print("-" * 95)
for r in report_data:
    print(f"{r['name'][:43]:<45} | {r['pages']:<5} | {r['chunks']:<6} | {r['vectors']:<7} | {r['db']:<8} | {r['storage']:<8}")
