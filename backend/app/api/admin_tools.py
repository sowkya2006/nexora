"""
Admin Tools — RAG Re-ingestion & Diagnostics
=============================================
Endpoints:
  POST /admin/reingest-from-storage?start=0&end=5&clear=true
      Fetches PDFs from Supabase Storage, re-chunks with v2 chunker,
      embeds with HF API, upserts to Pinecone with CANONICAL metadata keys.

  GET  /admin/pinecone-stats
      Returns total vector count + namespace breakdown.

  POST /admin/test-query?q=...
      Returns raw Pinecone scores for a query — used for debugging.

Canonical metadata schema (matches what chat_service.py reads):
  document_name  — human-readable doc title  (e.g. "Course Catalog & Programmes")
  document_id    — UUID of the document
  category       — document category string
  file_name      — PDF filename
  file_url       — Supabase public URL
  page           — dominant page number (int)
  page_number    — same as page (redundant copy for backward compat)
  chunk_number   — sequential chunk index within this document
  chunk_index    — same as chunk_number (redundant copy)
  text           — chunk text (max 500 chars stored; full text used for embedding)
"""
import uuid
import logging
from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_admin
from app.schemas.auth import AdminUser

logger = logging.getLogger(__name__)
router = APIRouter()

# ── Document registry ─────────────────────────────────────────────────────────
# (filename, canonical_title, category)
# canonical_title MUST match exactly what INTENT_DOCUMENT_MAP values use in chat_service.py
KB_FILES = [
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


def _build_vectors(doc_id: str, title: str, category: str,
                   filename: str, file_url: str,
                   chunk_dicts: list, embeddings: list) -> list:
    """
    Build Pinecone vector dicts using the CANONICAL metadata schema.
    Both old keys (title / page_number / chunk_number) AND new keys
    (document_name / page / chunk_index) are stored so chat_service
    works regardless of which keys it tries first.
    """
    vectors = []
    for i, (chunk, emb) in enumerate(zip(chunk_dicts, embeddings)):
        page_num   = chunk.get("page_number", chunk.get("page", 1))
        chunk_num  = chunk.get("chunk_number", chunk.get("chunk_index", i))
        text       = chunk.get("text", "")

        metadata = {
            # ── canonical keys (read by chat_service._get_meta) ──────────
            "document_name":  title,          # primary key used by chat_service
            "title":          title,          # backward compat alias
            "document_id":    doc_id,
            "category":       category,
            "file_name":      filename,
            "file_url":       file_url,
            "page":           page_num,       # primary page key
            "page_number":    page_num,       # backward compat alias
            "chunk_number":   chunk_num,      # primary chunk key
            "chunk_index":    chunk_num,      # backward compat alias
            "text":           text[:800],     # stored snippet (full text used for embedding)
        }
        vectors.append({
            "id":     f"{doc_id}_chunk_{chunk_num}",
            "values": emb,
            "metadata": metadata,
        })
    return vectors


@router.post("/admin/reingest-from-storage")
async def reingest_from_storage(
    start: int = 0,
    end: int = 5,
    clear: bool = False,
    _admin: AdminUser = Depends(get_current_admin),
):
    """
    Re-ingest a batch of PDFs from Supabase Storage using HF API embeddings.
    Uses the v2 semantic chunker (900 words, 150-word overlap).

    Call in 3 batches:
      ?start=0&end=5&clear=true    (clears Pinecone first)
      ?start=5&end=10&clear=false
      ?start=10&end=14&clear=false
    """
    import httpx as hx
    from app.rag.pinecone_client import get_pinecone_index
    from app.rag.embeddings import generate_chunk_embeddings
    from app.services.pdf_processor import extract_text_by_page, semantic_chunking
    from app.config import settings

    SUPABASE_URL = settings.supabase_url.strip()
    pinecone_idx = get_pinecone_index()

    if clear:
        try:
            pinecone_idx.delete(delete_all=True)
            logger.info("[Reingest] Cleared all Pinecone vectors")
        except Exception as e:
            logger.warning(f"[Reingest] Clear warning: {e}")

    batch   = KB_FILES[start:end]
    total   = 0
    results = []

    for filename, title, category in batch:
        # ── Download PDF from Supabase Storage ────────────────────────────
        storage_url = f"{SUPABASE_URL}/storage/v1/object/public/documents/pdfs/{filename}"
        try:
            resp = hx.get(storage_url, timeout=30, follow_redirects=True)
            if resp.status_code != 200:
                logger.error(f"[Reingest] Download failed {filename}: HTTP {resp.status_code}")
                results.append({"file": filename, "status": f"download_failed_{resp.status_code}"})
                continue
            file_bytes = resp.content
        except Exception as e:
            logger.error(f"[Reingest] Network error {filename}: {e}")
            results.append({"file": filename, "status": "network_error", "error": str(e)[:100]})
            continue

        try:
            # ── Extract text ───────────────────────────────────────────────
            pages = extract_text_by_page(file_bytes)
            total_page_words = sum(len(t.split()) for _, t in pages)
            logger.info(f"[Reingest] {filename}: {len(pages)} pages, {total_page_words} words")

            # ── Chunk with v2 chunker (900 words, 150 overlap) ─────────────
            chunk_dicts = semantic_chunking(pages, chunk_size_words=900, overlap_words=150)
            logger.info(f"[Reingest] {filename}: {len(chunk_dicts)} chunks "
                        f"(avg {total_page_words // max(len(chunk_dicts), 1)} words/chunk)")

            if not chunk_dicts:
                results.append({"file": filename, "status": "no_chunks"})
                continue

            # ── Embed with HF API (same model used at query time) ──────────
            chunk_texts = [c["text"] for c in chunk_dicts]
            embeddings  = generate_chunk_embeddings(chunk_texts)

            if len(embeddings) != len(chunk_dicts):
                raise ValueError(f"Embedding count mismatch: {len(embeddings)} vs {len(chunk_dicts)}")

            # ── Build vectors with canonical metadata ──────────────────────
            doc_id  = str(uuid.uuid4())
            vectors = _build_vectors(doc_id, title, category,
                                     filename, storage_url,
                                     chunk_dicts, embeddings)

            # ── Upsert to Pinecone in batches of 50 ───────────────────────
            for i in range(0, len(vectors), 50):
                pinecone_idx.upsert(vectors=vectors[i:i + 50])

            total += len(chunk_dicts)
            logger.info(f"[Reingest] {filename}: upserted {len(vectors)} vectors OK")
            results.append({
                "file":   filename,
                "title":  title,
                "chunks": len(chunk_dicts),
                "vectors": len(vectors),
                "status": "ok",
            })

        except Exception as e:
            logger.error(f"[Reingest] Processing error {filename}: {e}")
            results.append({"file": filename, "status": "error", "error": str(e)[:200]})

    return {
        "status":                  "batch_complete",
        "batch":                   f"{start}-{end}",
        "total_vectors_this_batch": total,
        "results":                 results,
    }


@router.get("/admin/pinecone-stats")
async def pinecone_stats(_admin: AdminUser = Depends(get_current_admin)):
    """Return Pinecone index statistics."""
    from app.rag.pinecone_client import get_pinecone_index
    try:
        idx   = get_pinecone_index()
        stats = idx.describe_index_stats()
        return {
            "status":        "ok",
            "total_vectors": stats.total_vector_count,
            "namespaces":    {k: v.vector_count for k, v in stats.namespaces.items()},
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/admin/test-query")
async def test_query(
    q: str = "What are the hostel facilities?",
    _admin: AdminUser = Depends(get_current_admin),
):
    """
    Debug endpoint: returns raw Pinecone scores + metadata for a query.
    Use this to verify retrieval before asking through the chat endpoint.
    """
    from app.rag.pinecone_client import get_pinecone_index
    from app.rag.embeddings import generate_chunk_embeddings
    try:
        vec     = generate_chunk_embeddings([q])[0]
        idx     = get_pinecone_index()
        results = idx.query(vector=vec, top_k=10, include_metadata=True)
        matches = []
        for m in results.matches:
            meta = m.metadata or {}
            matches.append({
                "score":         round(m.score, 5),
                "document_name": meta.get("document_name", meta.get("title", "?")),
                "page":          meta.get("page", meta.get("page_number", "?")),
                "chunk_number":  meta.get("chunk_number", meta.get("chunk_index", "?")),
                "text_preview":  meta.get("text", "")[:120],
            })
        return {
            "query":          q,
            "embedding_dim":  len(vec),
            "top_10_matches": matches,
        }
    except Exception as e:
        return {"error": str(e)}
