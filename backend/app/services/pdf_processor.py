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
    chunk_size_words: int = 600,
    overlap_words: int = 100
) -> List[Dict[str, Any]]:
    """
    Splits text into chunks of 500-800 words (~500-800 tokens) with 100 word overlap (~100 tokens).
    Preserves page number metadata for each chunk.
    """
    chunks = []
    chunk_counter = 0

    for page_num, text in pages_text:
        words = text.split()
        if not words:
            continue
        
        if len(words) <= chunk_size_words:
            chunk_counter += 1
            chunks.append({
                "chunk_number": chunk_counter,
                "page_number": page_num,
                "text": text,
            })
        else:
            step = chunk_size_words - overlap_words
            for start_idx in range(0, len(words), step):
                end_idx = min(start_idx + chunk_size_words, len(words))
                chunk_words = words[start_idx:end_idx]
                chunk_str = " ".join(chunk_words)

                if chunk_str.strip():
                    chunk_counter += 1
                    chunks.append({
                        "chunk_number": chunk_counter,
                        "page_number": page_num,
                        "text": chunk_str,
                    })

                if end_idx >= len(words):
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
