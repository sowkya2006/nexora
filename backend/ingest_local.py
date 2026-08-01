"""
Ingest all PDFs using the LOCAL sentence-transformers model.
Run this once to populate Pinecone with real embeddings.
python ingest_local.py
"""
import os, sys, uuid, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Use local model directly — bypass the HF API
from sentence_transformers import SentenceTransformer
from app.rag.pinecone_client import get_pinecone_index
from app.services.pdf_processor import extract_text_by_page, semantic_chunking
from app.database.supabase import get_supabase_client
from app.config import settings

print("Loading local embedding model...")
model = SentenceTransformer("BAAI/bge-large-en-v1.5", device="cpu")
print("Model loaded.")

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

def embed(texts):
    return model.encode(texts, normalize_embeddings=True, show_progress_bar=False).tolist()

def ingest():
    pinecone_idx = get_pinecone_index()
    supabase = get_supabase_client()

    print("Clearing Pinecone...")
    try:
        pinecone_idx.delete(delete_all=True)
        print("Cleared.")
    except Exception as e:
        print(f"Clear note: {e}")

    total = 0

    for filename, title, category in DOCS:
        pdf_path = os.path.join(KB, filename)
        if not os.path.exists(pdf_path):
            print(f"SKIP: {filename}")
            continue

        print(f"\n{filename}")
        with open(pdf_path, "rb") as f:
            file_bytes = f.read()

        pages = extract_text_by_page(file_bytes)
        chunk_dicts = semantic_chunking(pages)
        chunks = [c["text"] for c in chunk_dicts]
        chunk_pages = [c["page_number"] for c in chunk_dicts]
        print(f"  {len(pages)} pages, {len(chunks)} chunks")

        if not chunks:
            continue

        embeddings = embed(chunks)
        doc_id = str(uuid.uuid4())

        vectors = []
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            vectors.append({
                "id": f"{doc_id}_chunk_{i}",
                "values": emb,
                "metadata": {
                    "document_id": doc_id,
                    "document_name": title,
                    "category": category,
                    "file_name": filename,
                    "page": chunk_pages[i],
                    "text": chunk[:500],
                    "chunk_index": i,
                }
            })

        for i in range(0, len(vectors), 50):
            pinecone_idx.upsert(vectors=vectors[i:i+50])
        print(f"  Upserted {len(vectors)} vectors")

        # Save to Supabase
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        doc_data = {
            "id": doc_id,
            "title": title,
            "category": category,
            "file_url": f"https://nexora-backend-three.vercel.app/knowledge_base/{filename}",
            "file_name": filename,
            "status": "indexed",
            "created_at": now,
            "updated_at": now,
        }
        try:
            supabase.table("documents").upsert(doc_data).execute()
        except Exception as e:
            print(f"  Supabase note: {e}")

        total += len(chunks)

    print(f"\nDONE. Total vectors: {total}")

if __name__ == "__main__":
    ingest()
