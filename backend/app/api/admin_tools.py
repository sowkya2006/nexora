"""
One-time admin tools endpoint.
Triggered via POST /api/v1/admin/reingest to re-index all PDFs from knowledge_base.
This runs ON the server (Vercel) so it uses the same HF embeddings as queries.
"""
import os
import uuid
import datetime
import logging
from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_admin
from app.schemas.auth import AdminUser

logger = logging.getLogger(__name__)
router = APIRouter()

KB_FILES = [
    ("Admission_Handbook_2026.pdf",          "Admission Handbook 2026",            "Admissions"),
    ("Fee_Structure_2026.pdf",               "Fee Structure 2026-27",              "Finance"),
    ("Hostel_Accommodation_Guide.pdf",       "Hostel & Accommodation Guide",       "Hostel"),
    ("Placement_Report_2026.pdf",            "Placement Report 2026",              "Placements"),
    ("Academic_Regulations_2026.pdf",        "Academic Regulations 2026",          "Academics"),
    ("Scholarships_Financial_Aid_2026.pdf",  "Scholarships & Financial Aid 2026",  "Scholarships"),
    ("Course_Catalog_and_Programs.pdf",      "Course Catalog & Programmes",        "Academics"),
    ("Academic_Calendar_2026.pdf",           "Academic Calendar 2026-27",          "Academics"),
    ("Library_Guide_2026.pdf",               "Library Guide 2026",                 "Library"),
    ("Transport_Guide_2026.pdf",             "Transport Guide 2026",               "Transport"),
    ("Research_Innovation_Handbook.pdf",     "Research & Innovation Handbook",     "Research"),
    ("Department_Handbook_CSE.pdf",          "Department Handbook: CSE",           "Departments"),
    ("Student_Handbook_Code_of_Conduct.pdf", "Student Handbook & Code of Conduct", "General"),
    ("Campus_Facilities_Guide.pdf",          "Campus Facilities Guide",            "Campus"),
]


def _do_reingest():
    """Runs in background. Reads PDFs from knowledge_base and re-indexes into Pinecone."""
    from pathlib import Path
    from app.rag.pinecone_client import get_pinecone_index
    from app.rag.embeddings import generate_chunk_embeddings
    from app.services.pdf_processor import extract_text_by_page, semantic_chunking

    # knowledge_base is 2 levels up from backend/app/api/
    kb_dir = Path(__file__).parent.parent.parent.parent / "knowledge_base"
    logger.info(f"Reingest: looking for PDFs in {kb_dir}")

    pinecone_idx = get_pinecone_index()

    # Clear existing
    try:
        pinecone_idx.delete(delete_all=True)
        logger.info("Reingest: cleared Pinecone")
    except Exception as e:
        logger.warning(f"Reingest: clear warning: {e}")

    total = 0
    for filename, title, category in KB_FILES:
        pdf_path = kb_dir / filename
        if not pdf_path.exists():
            logger.warning(f"Reingest: not found: {filename}")
            continue

        try:
            file_bytes = pdf_path.read_bytes()
            pages = extract_text_by_page(file_bytes)
            chunk_dicts = semantic_chunking(pages)
            chunks = [c["text"] for c in chunk_dicts]
            chunk_pages = [c["page_number"] for c in chunk_dicts]

            if not chunks:
                continue

            embeddings = generate_chunk_embeddings(chunks)
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

            total += len(chunks)
            logger.info(f"Reingest: {filename} -> {len(chunks)} chunks")
        except Exception as e:
            logger.error(f"Reingest error for {filename}: {e}")

    logger.info(f"Reingest complete. Total vectors: {total}")


@router.post("/admin/reingest")
async def trigger_reingest(
    _admin: AdminUser = Depends(get_current_admin),
):
    """
    Synchronously re-ingest all knowledge_base PDFs into Pinecone.
    Processes one file at a time to stay within Vercel timeout limits.
    """
    from pathlib import Path
    from app.rag.pinecone_client import get_pinecone_index
    from app.rag.embeddings import generate_chunk_embeddings
    from app.services.pdf_processor import extract_text_by_page, semantic_chunking

    kb_dir = Path(__file__).parent.parent.parent.parent / "knowledge_base"
    pinecone_idx = get_pinecone_index()

    # Process only first 3 files per call to stay within 60s Vercel limit
    # Call multiple times to index all files
    import json
    from fastapi import Query as FQuery

    try:
        pinecone_idx.delete(delete_all=True)
    except Exception as e:
        logger.warning(f"Clear: {e}")

    total = 0
    results = []

    for filename, title, category in KB_FILES[:5]:
        pdf_path = kb_dir / filename
        if not pdf_path.exists():
            results.append({"file": filename, "status": "not_found"})
            continue
        try:
            file_bytes = pdf_path.read_bytes()
            pages = extract_text_by_page(file_bytes)
            chunk_dicts = semantic_chunking(pages)
            chunks = [c["text"] for c in chunk_dicts]
            chunk_pages = [c["page_number"] for c in chunk_dicts]
            if not chunks:
                continue
            embeddings = generate_chunk_embeddings(chunks)
            doc_id = str(uuid.uuid4())
            vectors = [{"id": f"{doc_id}_chunk_{i}", "values": emb, "metadata": {
                "document_id": doc_id, "document_name": title, "category": category,
                "file_name": filename, "page": chunk_pages[i], "text": chunk[:500], "chunk_index": i,
            }} for i, (chunk, emb) in enumerate(zip(chunks, embeddings))]
            for i in range(0, len(vectors), 50):
                pinecone_idx.upsert(vectors=vectors[i:i+50])
            total += len(chunks)
            results.append({"file": filename, "chunks": len(chunks), "status": "ok"})
        except Exception as e:
            results.append({"file": filename, "status": "error", "error": str(e)[:100]})

    return {"status": "batch_complete", "total_vectors": total, "results": results}


@router.post("/admin/reingest-batch")
async def trigger_reingest_batch(
    start: int = 0,
    end: int = 5,
    clear: bool = False,
    _admin: AdminUser = Depends(get_current_admin),
):
    """
    Re-ingest a batch of PDFs (start to end index from KB_FILES list).
    Call multiple times: start=0&end=5, start=5&end=10, start=10&end=14
    """
    from pathlib import Path
    from app.rag.pinecone_client import get_pinecone_index
    from app.rag.embeddings import generate_chunk_embeddings
    from app.services.pdf_processor import extract_text_by_page, semantic_chunking

    kb_dir = Path(__file__).parent.parent.parent.parent / "knowledge_base"
    pinecone_idx = get_pinecone_index()

    if clear:
        try:
            pinecone_idx.delete(delete_all=True)
        except Exception as e:
            logger.warning(f"Clear: {e}")

    batch = KB_FILES[start:end]
    total = 0
    results = []

    for filename, title, category in batch:
        pdf_path = kb_dir / filename
        if not pdf_path.exists():
            results.append({"file": filename, "status": "not_found"})
            continue
        try:
            file_bytes = pdf_path.read_bytes()
            pages = extract_text_by_page(file_bytes)
            chunk_dicts = semantic_chunking(pages)
            chunks = [c["text"] for c in chunk_dicts]
            chunk_pages = [c["page_number"] for c in chunk_dicts]
            if not chunks:
                continue
            embeddings = generate_chunk_embeddings(chunks)
            doc_id = str(uuid.uuid4())
            vectors = [{"id": f"{doc_id}_chunk_{i}", "values": emb, "metadata": {
                "document_id": doc_id, "document_name": title, "category": category,
                "file_name": filename, "page": chunk_pages[i], "text": chunk[:500], "chunk_index": i,
            }} for i, (chunk, emb) in enumerate(zip(chunks, embeddings))]
            for i in range(0, len(vectors), 50):
                pinecone_idx.upsert(vectors=vectors[i:i+50])
            total += len(chunks)
            results.append({"file": filename, "chunks": len(chunks), "status": "ok"})
        except Exception as e:
            results.append({"file": filename, "status": "error", "error": str(e)[:100]})

    return {"status": "batch_complete", "batch": f"{start}-{end}", "total_vectors": total, "results": results}


@router.get("/admin/pinecone-stats")
async def pinecone_stats(_admin: AdminUser = Depends(get_current_admin)):
    """Check current Pinecone index stats."""
    from app.rag.pinecone_client import get_pinecone_index
    try:
        idx = get_pinecone_index()
        stats = idx.describe_index_stats()
        return {
            "status": "ok",
            "total_vectors": stats.total_vector_count,
            "namespaces": {k: v.vector_count for k, v in stats.namespaces.items()}
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/admin/test-query")
async def test_query(
    q: str = "What are the hostel facilities?",
    _admin: AdminUser = Depends(get_current_admin),
):
    """Test Pinecone query with raw scores — debug endpoint."""
    from app.rag.pinecone_client import get_pinecone_index
    from app.rag.embeddings import generate_chunk_embeddings
    try:
        vec = generate_chunk_embeddings([q])[0]
        idx = get_pinecone_index()
        results = idx.query(vector=vec, top_k=5, include_metadata=True)
        matches = []
        for m in results.matches:
            matches.append({
                "score": round(m.score, 4),
                "doc": m.metadata.get("document_name", "?") if m.metadata else "?",
                "page": m.metadata.get("page", "?") if m.metadata else "?",
                "text_preview": (m.metadata.get("text", "")[:80] if m.metadata else ""),
            })
        return {
            "query": q,
            "embedding_dim": len(vec),
            "top_matches": matches,
        }
    except Exception as e:
        return {"error": str(e)}
