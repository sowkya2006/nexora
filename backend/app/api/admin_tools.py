"""
One-time admin tools endpoint.
Triggered via POST /api/v1/admin/reingest to re-index all PDFs from knowledge_base.
This runs ON the server (Vercel) so it uses the same HF embeddings as queries.
"""
import os
import uuid
import datetime
import logging
from fastapi import APIRouter, Depends, BackgroundTasks
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
    background_tasks: BackgroundTasks,
    _admin: AdminUser = Depends(get_current_admin),
):
    """
    Trigger re-ingestion of all knowledge_base PDFs into Pinecone.
    Uses the same HF API embeddings as chat queries.
    Admin only.
    """
    background_tasks.add_task(_do_reingest)
    return {
        "status": "started",
        "message": "Re-ingestion started in background. All PDFs will be re-indexed using HF embeddings. Check Pinecone stats in ~2 minutes.",
        "files": len(KB_FILES)
    }


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
