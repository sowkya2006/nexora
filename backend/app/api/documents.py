from fastapi import APIRouter, Depends, Query, UploadFile, File, Form, BackgroundTasks, HTTPException, status
from typing import Optional

from app.auth.dependencies import get_current_admin
from app.schemas.api import DocumentCreate, DocumentUpdate, DocumentResponse, DocumentListResponse
from app.schemas.auth import AdminUser
from app.services.document_service import DocumentService

router = APIRouter()


@router.get("/", response_model=DocumentListResponse)
async def list_documents(
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    """List all university documents with optional category and status filters."""
    return DocumentService.list_documents(category=category, status=status)


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str):
    """Get details of a single document by ID."""
    return DocumentService.get_document(document_id)


@router.post("/upload-pdf", response_model=DocumentResponse)
async def upload_pdf_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: str = Form(...),
    category: str = Form(...),
    description: Optional[str] = Form(None),
    admin: AdminUser = Depends(get_current_admin),
):
    """Upload a PDF document (Admin only). Initiates background RAG processing."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid file format. Only PDF files (.pdf) are allowed.")
    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Uploaded PDF file is empty.")
    try:
        return DocumentService.upload_and_process_pdf(
            file_bytes=file_bytes, filename=file.filename,
            title=title, category=category, description=description,
            uploaded_by=admin.id, background_tasks=background_tasks,
        )
    except ValueError as val_err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(val_err))
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to process upload: {str(err)}")


@router.post("/{document_id}/reprocess", response_model=DocumentResponse)
async def reprocess_document(
    document_id: str,
    background_tasks: BackgroundTasks,
    _admin: AdminUser = Depends(get_current_admin),
):
    """Re-run full RAG pipeline on an existing document (Admin only).
    Fetches file from Supabase Storage and re-indexes into Pinecone."""
    return DocumentService.reprocess_document(document_id=document_id, background_tasks=background_tasks)


@router.post("/", response_model=DocumentResponse)
async def create_document(
    payload: DocumentCreate,
    admin: AdminUser = Depends(get_current_admin),
):
    """Create document metadata record (Admin only)."""
    return DocumentService.create_document(payload, uploaded_by=admin.id)


@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    payload: DocumentUpdate,
    _admin: AdminUser = Depends(get_current_admin),
):
    """Update document metadata (Admin only)."""
    return DocumentService.update_document(document_id, payload)


@router.delete("/{document_id}", response_model=DocumentResponse)
async def delete_document(
    document_id: str,
    _admin: AdminUser = Depends(get_current_admin),
):
    """Delete a document completely — removes from Storage, Pinecone, and DB."""
    return DocumentService.delete_document(document_id)
