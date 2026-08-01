"""
Upload all 14 PDFs to Supabase Storage AND index them into Pinecone.
Run this ONCE from local machine.
Embeddings: local sentence-transformers model (same as query on Vercel via HF API)
"""
import os, sys, uuid, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from sentence_transformers import SentenceTransformer
from app.rag.pinecone_client import get_pinecone_index
from app.services.pdf_processor import extract_text_by_page, semantic_chunking
from app.database.supabase import get_supabase_client
from app.config import settings

print("Loading local embedding model...")
model = SentenceTransformer("BAAI/bge-large-en-v1.5", device="cpu")
print("Model loaded.")

KB = os.path.join(os.path.dirname(__file__), "..", "knowledge_base")
SUPABASE_URL = settings.supabase_url

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

def upload_to_storage(supabase, file_bytes, filename):
    """Upload PDF to Supabase Storage bucket 'documents' and return public URL."""
    storage_path = f"pdfs/{filename}"
    try:
        # Delete existing file first
        try:
            supabase.storage.from_("documents").remove([storage_path])
        except:
            pass
        # Upload
        supabase.storage.from_("documents").upload(
            path=storage_path,
            file=file_bytes,
            file_options={"content-type": "application/pdf", "upsert": "true"}
        )
        # Get public URL
        public_url = supabase.storage.from_("documents").get_public_url(storage_path)
        return public_url
    except Exception as e:
        print(f"  Storage upload note: {e}")
        return f"{SUPABASE_URL}/storage/v1/object/public/documents/{storage_path}"

def run():
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
            print(f"SKIP (not found): {filename}")
            continue

        print(f"\n{filename}")
        with open(pdf_path, "rb") as f:
            file_bytes = f.read()

        # Upload to Supabase Storage
        print(f"  Uploading to Supabase Storage...")
        public_url = upload_to_storage(supabase, file_bytes, filename)
        print(f"  URL: {public_url[:60]}...")

        # Extract and chunk
        pages = extract_text_by_page(file_bytes)
        chunk_dicts = semantic_chunking(pages)
        chunks = [c["text"] for c in chunk_dicts]
        chunk_pages = [c["page_number"] for c in chunk_dicts]
        print(f"  {len(pages)} pages, {len(chunks)} chunks")

        if not chunks:
            continue

        # Embed
        embeddings = embed(chunks)
        doc_id = str(uuid.uuid4())

        # Build vectors
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
                    "file_url": public_url,
                    "page": chunk_pages[i],
                    "text": chunk[:500],
                    "chunk_index": i,
                }
            })

        # Upsert to Pinecone
        for i in range(0, len(vectors), 50):
            pinecone_idx.upsert(vectors=vectors[i:i+50])
        print(f"  Upserted {len(vectors)} vectors")

        # Save to Supabase documents table
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        doc_data = {
            "id": doc_id,
            "title": title,
            "category": category,
            "file_url": public_url,
            "file_name": filename,
            "status": "indexed",
            "created_at": now,
            "updated_at": now,
        }
        try:
            supabase.table("documents").upsert(doc_data).execute()
            print(f"  Saved to Supabase")
        except Exception as e:
            print(f"  Supabase note: {e}")

        total += len(chunks)

    print(f"\nDONE. Total vectors in Pinecone: {total}")
    print("Verifying...")
    stats = pinecone_idx.describe_index_stats()
    print(f"Pinecone total vectors: {stats.total_vector_count}")

if __name__ == "__main__":
    run()
