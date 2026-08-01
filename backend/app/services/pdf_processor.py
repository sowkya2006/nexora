import fitz  # PyMuPDF
import re
import datetime
import logging
from typing import List, Dict, Any, Tuple
from app.config import settings
from app.database.supabase import get_supabase_client
from app.rag.pinecone_client import get_pinecone_index
from app.rag.embeddings import generate_chunk_embeddings

logger = logging.getLogger(__name__)

MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB limit


def validate_pdf_file(file_content: bytes, filename: str) -> None:
    """
    Validates file extension, size, and checks for corrupted PDF headers.
    """
    if not filename.lower().endswith(".pdf"):
        raise ValueError("Invalid file format. Only PDF files are allowed.")
    
    if len(file_content) > MAX_FILE_SIZE_BYTES:
        raise ValueError(f"File size exceeds maximum limit of {MAX_FILE_SIZE_BYTES // (1024*1024)}MB.")

    if not file_content.startswith(b"%PDF"):
        raise ValueError("Corrupted PDF file. PDF header missing or invalid.")


def extract_text_by_page(file_content: bytes) -> List[Tuple[int, str]]:
    """
    Extracts text page by page from PDF bytes using PyMuPDF (fitz).
    Returns a list of tuples: (page_number [1-indexed], page_text).
    """
    pages_text = []
    try:
        doc = fitz.open(stream=file_content, filetype="pdf")
        if doc.is_encrypted:
            raise ValueError("Encrypted or password-protected PDF files are not supported.")
        
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            raw_text = page.get_text("text")
            cleaned_text = clean_extracted_text(raw_text)
            if cleaned_text:
                pages_text.append((page_idx + 1, cleaned_text))
        
        doc.close()
    except Exception as e:
        logger.error(f"PyMuPDF extraction failed: {str(e)}")
        raise ValueError(f"Could not parse PDF content: {str(e)}")
    
    if not pages_text:
        raise ValueError("PDF file contains no readable text content.")
    
    return pages_text


def clean_extracted_text(text: str) -> str:
    """
    Cleans raw PDF extracted text by removing control chars, double spaces, and normalizing linebreaks.
    """
    if not text:
        return ""
    # Normalize unicode whitespace
    text = re.sub(r'[\r\t\f\v]', ' ', text)
    # Collapse multiple consecutive newlines to maximum of 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Collapse multiple consecutive spaces
    text = re.sub(r' +', ' ', text)
    return text.strip()


def semantic_chunking(
    pages_text: List[Tuple[int, str]],
    chunk_size_words: int = 900,
    overlap_words: int = 150,
) -> List[Dict[str, Any]]:
    """
    Semantic chunking v2:
    - Target 800-1000 words per chunk (default 900)
    - 150-word overlap between consecutive chunks
    - Never splits a heading from its first paragraph
    - Merges very short pages with the next page before chunking
    - Returns list of dicts: {chunk_number, page_number, text, word_count}
    """
    # ── Step 1: merge short pages into the next page ─────────────────────
    # If a page has fewer than 80 words it's almost certainly just a header
    # page — merge it into the following page so it carries context.
    MIN_PAGE_WORDS = 80
    merged_pages: List[Tuple[int, str]] = []
    carry_text = ""
    carry_page = 1

    for page_num, text in pages_text:
        words = text.split()
        if len(words) < MIN_PAGE_WORDS:
            carry_text = carry_text + " " + text if carry_text else text
            carry_page = page_num
        else:
            if carry_text:
                text = carry_text + " " + text
                carry_text = ""
            merged_pages.append((page_num, text.strip()))

    # flush any remaining carry
    if carry_text:
        if merged_pages:
            prev_pg, prev_txt = merged_pages[-1]
            merged_pages[-1] = (prev_pg, prev_txt + " " + carry_text)
        else:
            merged_pages.append((carry_page, carry_text))

    if not merged_pages:
        merged_pages = pages_text  # fallback: use original if everything was short

    # ── Step 2: detect heading lines ─────────────────────────────────────
    # A line is considered a heading if it is short (<= 12 words), ends without
    # a period/comma, and is followed by body text.
    HEADING_RE = re.compile(
        r'^(\s*(?:#+\s+)?[A-Z0-9][A-Z0-9 &:,\-\.\/]{0,80})\s*$',
        re.MULTILINE
    )

    def _is_heading_line(line: str) -> bool:
        stripped = line.strip()
        if not stripped:
            return False
        word_count = len(stripped.split())
        ends_with_sentence = stripped.endswith(('.', ',', ';', ':', '?', '!'))
        return word_count <= 12 and not ends_with_sentence

    # ── Step 3: build word list keeping page-boundary markers ────────────
    # We work on a flat list of (word, page_number) pairs so we can track
    # which page each chunk's majority content came from.
    word_page_list: List[Tuple[str, int]] = []
    for page_num, text in merged_pages:
        for word in text.split():
            word_page_list.append((word, page_num))

    if not word_page_list:
        return []

    total_words = len(word_page_list)
    chunks: List[Dict[str, Any]] = []
    chunk_counter = 0
    start = 0

    while start < total_words:
        end = min(start + chunk_size_words, total_words)

        # ── Do not break mid-heading ──────────────────────────────────────
        # Look back up to 15 words from the cut point to see if we're
        # inside a heading; if so, push the cut to before the heading.
        if end < total_words:
            # Reconstruct the last 15 words as a string to test for headings
            lookback_start = max(end - 15, start)
            lookback_text  = " ".join(w for w, _ in word_page_list[lookback_start:end])
            lines = lookback_text.split("\n")
            last_line = lines[-1] if lines else ""
            if _is_heading_line(last_line):
                # Move cut point back to before this heading
                words_in_heading = len(last_line.split())
                end = max(end - words_in_heading, start + 1)

        chunk_words = [w for w, _ in word_page_list[start:end]]
        chunk_text  = " ".join(chunk_words).strip()

        if chunk_text:
            # Dominant page = page that appears most in this chunk
            page_counts: Dict[int, int] = {}
            for _, pg in word_page_list[start:end]:
                page_counts[pg] = page_counts.get(pg, 0) + 1
            dominant_page = max(page_counts, key=lambda p: page_counts[p])

            chunk_counter += 1
            chunks.append({
                "chunk_number": chunk_counter,
                "page_number":  dominant_page,
                "text":         chunk_text,
                "word_count":   len(chunk_words),
            })

        # Advance by chunk_size - overlap (sliding window)
        step = chunk_size_words - overlap_words
        start += step
        if start >= total_words:
            break

    return chunks


def process_and_index_document(
    document_id: str,
    file_bytes: bytes,
    title: str,
    category: str,
    filename: str
) -> None:
    """
    Full background processing task:
    1. Validate PDF & extract text via PyMuPDF
    2. Clean text & generate 500-800 word chunks with 100 word overlap
    3. Generate 1024-dimensional embeddings using BAAI/bge-large-en-v1.5
    4. Upsert vectors with metadata to Pinecone index 'nexora-university'
    5. Update document status in Supabase (uploaded -> processing -> indexed/failed)
    """
    supabase = get_supabase_client()
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

    try:
        # Step A: Update status to 'processing'
        logger.info(f"Starting processing for document ID: {document_id}")
        supabase.table("documents").update({"status": "processing"}).eq("id", document_id).execute()

        # Step B: Validate PDF & Extract Text
        validate_pdf_file(file_bytes, filename)
        pages_text = extract_text_by_page(file_bytes)

        # Step C: Semantic Chunking
        chunks = semantic_chunking(pages_text, chunk_size_words=600, overlap_words=100)
        logger.info(f"Document '{title}' split into {len(chunks)} chunks.")

        if not chunks:
            raise ValueError("No valid text chunks generated from PDF.")

        # Step D: Generate Embeddings via BAAI/bge-large-en-v1.5
        chunk_texts = [c["text"] for c in chunks]
        embeddings = generate_chunk_embeddings(chunk_texts)

        # Step E: Prepare Pinecone Vectors with Metadata
        vectors_to_upsert = []
        for i, chunk in enumerate(chunks):
            vector_id = f"{document_id}#chunk_{chunk['chunk_number']}"
            metadata = {
                "document_id": document_id,
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

        # Step F: Batch Upsert into Pinecone
        pinecone_index = get_pinecone_index()
        batch_size = 100
        for b_idx in range(0, len(vectors_to_upsert), batch_size):
            batch = vectors_to_upsert[b_idx: b_idx + batch_size]
            pinecone_index.upsert(vectors=batch)

        logger.info(f"Successfully upserted {len(vectors_to_upsert)} vectors to Pinecone for document {document_id}.")

        # Step G: Update status to 'indexed'
        try:
            supabase.table("documents").update({
                "status": "indexed",
                "chunk_count": len(chunks),
                "processed_at": now_iso,
                "updated_at": now_iso
            }).eq("id", document_id).execute()
        except Exception as schema_err:
            logger.warning(f"Full document metadata update failed, falling back to base status update: {schema_err}")
            supabase.table("documents").update({
                "status": "indexed",
                "updated_at": now_iso
            }).eq("id", document_id).execute()

    except Exception as err:
        logger.error(f"Error processing document {document_id}: {str(err)}")
        try:
            supabase.table("documents").update({
                "status": "failed",
                "updated_at": now_iso
            }).eq("id", document_id).execute()
        except Exception:
            pass


def delete_document_completely(document_id: str, file_path: str | None = None) -> bool:
    """
    Deletes document completely:
    1. Removes PDF file from Supabase Storage bucket 'documents'
    2. Deletes related vectors from Pinecone index 'nexora-university'
    3. Deletes record from Supabase 'documents' database table
    """
    supabase = get_supabase_client()

    # 1. Delete from Supabase Storage
    if file_path:
        try:
            supabase.storage.from_("documents").remove([file_path])
            logger.info(f"Removed file '{file_path}' from Supabase Storage bucket 'documents'.")
        except Exception as err:
            logger.warning(f"Storage file deletion warning: {err}")

    # 2. Delete vectors from Pinecone
    try:
        pinecone_index = get_pinecone_index()
        # Delete vectors matching metadata filter document_id
        pinecone_index.delete(filter={"document_id": document_id})
        logger.info(f"Deleted Pinecone vectors for document_id '{document_id}'.")
    except Exception as err:
        logger.warning(f"Pinecone vector deletion warning: {err}")

    # 3. Delete database record
    try:
        supabase.table("documents").delete().eq("id", document_id).execute()
        logger.info(f"Deleted database record for document_id '{document_id}'.")
        return True
    except Exception as err:
        logger.error(f"Database document deletion error: {err}")
        return False
