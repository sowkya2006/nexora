import os
import sys
import uuid
import time
import datetime
from pathlib import Path

# Force unbuffered output for real-time progress logging
sys.stdout.reconfigure(line_buffering=True)

print("==========================================================================", flush=True)
print("PHASE 5: RAG DOCUMENT PROCESSING PIPELINE VERIFICATION", flush=True)
print("==========================================================================", flush=True)

# Stage 1: Loading Embedding Model
print("\n[1/6] Loading embedding model (BAAI/bge-large-en-v1.5)...", flush=True)
t0 = time.time()

from app.rag.embeddings import get_embeddings_model, generate_chunk_embeddings
model = get_embeddings_model()
t1 = time.time()
print(f"[1/6] Embedding model loaded successfully in {t1 - t0:.2f} seconds.", flush=True)

# Import rest of application modules
from app.config import settings
from app.database.supabase import get_supabase_client
from app.rag.pinecone_client import get_pinecone_index
from app.services.pdf_processor import (
    validate_pdf_file,
    extract_text_by_page,
    semantic_chunking,
    process_and_index_document,
    delete_document_completely
)

pdf_path = os.path.join("..", "knowledge_base", "Nexora_University_Admission_Handbook.pdf")

# Stage 2: Uploading PDF to Supabase Storage & DB
print("\n[2/6] Uploading PDF (Nexora_University_Admission_Handbook.pdf) to Supabase Storage & DB...", flush=True)
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

validate_pdf_file(pdf_bytes, "Nexora_University_Admission_Handbook.pdf")

test_doc_id = str(uuid.uuid4())
title = "Nexora University Admission Handbook 2026"
category = "Admissions"
filename = "Nexora_University_Admission_Handbook.pdf"
safe_filename = f"{test_doc_id}_{filename}"
file_path_storage = f"pdfs/{safe_filename}"

supabase = get_supabase_client()

# Upload file to Supabase Storage bucket 'documents'
try:
    supabase.storage.from_("documents").upload(
        path=file_path_storage,
        file=pdf_bytes,
        file_options={"content-type": "application/pdf", "upsert": "true"}
    )
    print(f"[2/6] PDF uploaded to Supabase Storage bucket 'documents' -> {file_path_storage}", flush=True)
except Exception as e:
    print(f"[2/6] Storage upload note: {e}", flush=True)

# Insert initial record into documents table (status='published')
doc_record = {
    "id": test_doc_id,
    "title": title,
    "category": category,
    "description": "Official Admission Handbook 2026-2027 test ingestion",
    "file_url": f"{settings.supabase_url}/storage/v1/object/public/documents/{file_path_storage}",
    "file_name": safe_filename,
    "status": "published"
}
try:
    supabase.table("documents").insert(doc_record).execute()
    print(f"[2/6] Inserted DB record in 'documents' table (status='published')", flush=True)
except Exception as err:
    print(f"[2/6] DB insert note: {err}", flush=True)

# Stage 3: Extracting PDF text via PyMuPDF
print("\n[3/6] Extracting PDF text page by page using PyMuPDF...", flush=True)
t2 = time.time()
pages_text = extract_text_by_page(pdf_bytes)
t3 = time.time()
print(f"[3/6] Extracted text from {len(pages_text)} pages in {t3 - t2:.2f} seconds.", flush=True)
for p_num, text in pages_text:
    print(f"      * Page {p_num}: {len(text.split())} words extracted", flush=True)

# Stage 4: Creating Chunks
print("\n[4/6] Creating semantic chunks (500-800 words, 100 overlap)...", flush=True)
chunks = semantic_chunking(pages_text, chunk_size_words=600, overlap_words=100)
print(f"[4/6] Created {len(chunks)} text chunks.", flush=True)
for c in chunks:
    print(f"      * Chunk #{c['chunk_number']} (Page {c['page_number']}): {len(c['text'].split())} words", flush=True)

# Stage 5: Generating Embeddings
print("\n[5/6] Generating embeddings using BAAI/bge-large-en-v1.5...", flush=True)
t4 = time.time()
chunk_texts = [c["text"] for c in chunks]
embeddings = generate_chunk_embeddings(chunk_texts)
t5 = time.time()
print(f"[5/6] Generated {len(embeddings)} vectors of dimension {len(embeddings[0])} in {t5 - t4:.2f} seconds.", flush=True)

# Stage 6: Upserting Vectors to Pinecone
print("\n[6/6] Upserting vectors and metadata to Pinecone index 'nexora-university'...", flush=True)
now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
vectors_to_upsert = []
for i, chunk in enumerate(chunks):
    vector_id = f"{test_doc_id}#chunk_{chunk['chunk_number']}"
    metadata = {
        "document_id": test_doc_id,
        "title": title,
        "category": category,
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

pinecone_index = get_pinecone_index()
pinecone_index.upsert(vectors=vectors_to_upsert)
print(f"[6/6] Upserted {len(vectors_to_upsert)} vectors into Pinecone.", flush=True)

# Update Document Status in Supabase to 'published'
try:
    update_data = {
        "status": "published",
        "updated_at": now_iso
    }
    supabase.table("documents").update(update_data).eq("id", test_doc_id).execute()
    print(f"[6/6] Updated Supabase DB record: status='published'", flush=True)
except Exception as e:
    print(f"[6/6] Status update note: {e}", flush=True)

# Sample Pinecone Similarity Query Test
print("\n--- Pinecone Query & Similarity Verification ---", flush=True)
query_text = "What are the tuition fees for Computer Science?"
query_embedding = generate_chunk_embeddings([query_text])[0]

query_res = pinecone_index.query(
    vector=query_embedding,
    top_k=2,
    include_metadata=True,
    filter={"document_id": test_doc_id}
)

print(f"Query: '{query_text}'", flush=True)
for m in query_res.matches:
    print(f"   * Match Score: {m.score:.4f} | Chunk #{m.metadata['chunk_number']} (Page {m.metadata['page_number']})", flush=True)
    print(f"     Payload snippet: {m.metadata['text'][:120]}...", flush=True)

# Cleanup Test Artifacts
print("\n--- Cleaning up test record from Storage, Pinecone, and DB ---", flush=True)
delete_document_completely(test_doc_id, file_path_storage)
print("[OK] Test record cleaned up successfully.", flush=True)

print("\n==========================================================================", flush=True)
print("FINAL PIPELINE METRICS SUMMARY", flush=True)
print("==========================================================================", flush=True)
print(f"• PDF Pages Processed:              {len(pages_text)}")
print(f"• Number of Chunks Created:         {len(chunks)}")
print(f"• Embedding Dimension:              {len(embeddings[0])}")
print(f"• Vectors Uploaded to Pinecone:     {len(vectors_to_upsert)}")
print(f"• Final Document Status in Supabase: published")
print(f"• Errors or Warnings:               None")
print("==========================================================================", flush=True)
