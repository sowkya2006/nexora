"""
Ingest all 17 knowledge base PDFs into Pinecone using HuggingFace Inference API.
Run from the backend folder: python ingest_now.py
"""
import os, sys, uuid, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from app.rag.pinecone_client import get_pinecone_index
from app.rag.embeddings import generate_chunk_embeddings
from app.services.pdf_processor import extract_text_by_page, semantic_chunking
from app.database.supabase import get_supabase_client

KB = os.path.join(os.path.dirname(__file__), "..", "knowledge_base")

DOCS = [
    ("Admission_Handbook_2026.pdf",          "Admission Handbook 2026",               "Admissions"),
    ("Fee_Structure_2026.pdf",               "Fee Structure 2026-27",                 "Finance"),
    ("Hostel_Accommodation_Guide.pdf",       "Hostel & Accommodation Guide",          "Hostel"),
    ("Placement_Report_2026.pdf",            "Placement Report 2026",                 "Placements"),
    ("Academic_Regulations_2026.pdf",        "Academic Regulations 2026",             "Academics"),
    ("Scholarships_Financial_Aid_2026.pdf",  "Scholarships & Financial Aid 2026",     "Scholarships"),
    ("Course_Catalog_and_Programs.pdf",      "Course Catalog & Programmes",           "Academics"),
    ("Academic_Calendar_2026.pdf",           "Academic Calendar 2026-27",             "Academics"),
    ("Library_Guide_2026.pdf",               "Library Guide 2026",                    "Library"),
    ("Transport_Guide_2026.pdf",             "Transport Guide 2026",                  "Transport"),
    ("Research_Innovation_Handbook.pdf",     "Research & Innovation Handbook",        "Research"),
    ("Department_Handbook_CSE.pdf",          "Department Handbook: CSE",              "Departments"),
    ("Student_Handbook_Code_of_Conduct.pdf", "Student Handbook & Code of Conduct",    "General"),
    ("Campus_Facilities_Guide.pdf",          "Campus Facilities Guide",               "Campus"),
]

def ingest():
    pinecone_idx = get_pinecone_index()
    supabase = get_supabase_client()

    # Clear existing vectors
    print("Clearing existing Pinecone vectors...")
    try:
        pinecone_idx.delete(delete_all=True)
        print("Cleared.")
    except Exception as e:
        print(f"Clear warning: {e}")

    total_chunks = 0

    for filename, title, category in DOCS:
        pdf_path = os.path.join(KB, filename)
        if not os.path.exists(pdf_path):
            print(f"SKIP (not found): {filename}")
            continue

        print(f"\nProcessing: {filename}")
        with open(pdf_path, "rb") as f:
            file_bytes = f.read()

        try:
            pages = extract_text_by_page(file_bytes)
        except Exception as e:
            print(f"  Extract error: {e}")
            continue

        chunk_dicts = semantic_chunking(pages)
        chunks = [c["text"] for c in chunk_dicts]
        chunk_pages = [c["page_number"] for c in chunk_dicts]
        print(f"  {len(pages)} pages -> {len(chunks)} chunks")

        if not chunks:
            continue

        # Generate embeddings
        print(f"  Generating embeddings via HuggingFace API...")
        try:
            embeddings = generate_chunk_embeddings(chunks)
        except Exception as e:
            print(f"  Embedding error: {e}")
            continue

        # Build Pinecone vectors
        doc_id = str(uuid.uuid4())
        vectors = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            page_num = chunk_pages[i] if i < len(chunk_pages) else 1
            vectors.append({
                "id": f"{doc_id}_chunk_{i}",
                "values": embedding,
                "metadata": {
                    "document_id": doc_id,
                    "document_name": title,
                    "category": category,
                    "file_name": filename,
                    "page": page_num,
                    "text": chunk[:500],
                    "chunk_index": i,
                }
            })

        # Upsert to Pinecone in batches of 50
        batch_size = 50
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i+batch_size]
            pinecone_idx.upsert(vectors=batch)
        print(f"  Upserted {len(vectors)} vectors to Pinecone")

        # Save to Supabase
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        kb_base = "https://nexora-backend-three.vercel.app/knowledge_base"
        doc_data = {
            "id": doc_id,
            "title": title,
            "category": category,
            "file_url": f"{kb_base}/{filename}",
            "file_name": filename,
            "status": "indexed",
            "chunk_count": len(chunks),
            "created_at": now,
            "updated_at": now,
        }
        try:
            supabase.table("documents").upsert(doc_data).execute()
            print(f"  Saved to Supabase")
        except Exception as e:
            print(f"  Supabase warning: {e}")

        total_chunks += len(chunks)

    print(f"\n{'='*50}")
    print(f"DONE. Total chunks indexed: {total_chunks}")
    print(f"Run: python check_pinecone_stats.py to verify")

if __name__ == "__main__":
    ingest()
