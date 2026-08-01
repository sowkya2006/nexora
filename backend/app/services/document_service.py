import uuid
import datetime
import logging
from typing import List, Optional, Dict, Any
from fastapi import BackgroundTasks, HTTPException, status
from app.config import settings
from app.database.supabase import get_supabase_client
from app.schemas.api import DocumentCreate, DocumentUpdate, DocumentOut, DocumentListResponse, DocumentResponse
from app.services.pdf_processor import (
    validate_pdf_file,
    process_and_index_document,
    delete_document_completely
)

logger = logging.getLogger(__name__)


# All 17 knowledge-base PDFs served from the backend static mount at /knowledge_base/
_KB_BASE = "http://localhost:8000/knowledge_base"

MOCK_DOCUMENTS = [
    {"id":"doc-001","title":"Admission Handbook 2026","category":"Admissions",
     "description":"Complete undergraduate and postgraduate admissions guide 2026-27",
     "file_url":f"{_KB_BASE}/Admission_Handbook_2026.pdf","file_name":"Admission_Handbook_2026.pdf",
     "uploaded_by":"dev-admin","status":"indexed","chunk_count":48,
     "created_at":"2026-07-01T10:00:00Z","updated_at":"2026-07-01T10:00:00Z"},
    {"id":"doc-002","title":"Fee Structure 2026-27","category":"Finance",
     "description":"Tuition, hostel, mess and miscellaneous fee schedule",
     "file_url":f"{_KB_BASE}/Fee_Structure_2026.pdf","file_name":"Fee_Structure_2026.pdf",
     "uploaded_by":"dev-admin","status":"indexed","chunk_count":36,
     "created_at":"2026-07-01T10:01:00Z","updated_at":"2026-07-01T10:01:00Z"},
    {"id":"doc-003","title":"Hostel & Accommodation Guide","category":"Hostel",
     "description":"On-campus residential life, rules and mess schedule",
     "file_url":f"{_KB_BASE}/Hostel_Accommodation_Guide.pdf","file_name":"Hostel_Accommodation_Guide.pdf",
     "uploaded_by":"dev-admin","status":"indexed","chunk_count":42,
     "created_at":"2026-07-01T10:02:00Z","updated_at":"2026-07-01T10:02:00Z"},
    {"id":"doc-004","title":"Placement Report 2026","category":"Placements",
     "description":"Placement statistics, top recruiters and CDC resources",
     "file_url":f"{_KB_BASE}/Placement_Report_2026.pdf","file_name":"Placement_Report_2026.pdf",
     "uploaded_by":"dev-admin","status":"indexed","chunk_count":38,
     "created_at":"2026-07-01T10:03:00Z","updated_at":"2026-07-01T10:03:00Z"},
    {"id":"doc-005","title":"Academic Regulations 2026","category":"Academics",
     "description":"Grading, attendance, backlog and academic integrity policies",
     "file_url":f"{_KB_BASE}/Academic_Regulations_2026.pdf","file_name":"Academic_Regulations_2026.pdf",
     "uploaded_by":"dev-admin","status":"indexed","chunk_count":44,
     "created_at":"2026-07-01T10:04:00Z","updated_at":"2026-07-01T10:04:00Z"},
    {"id":"doc-006","title":"Scholarships & Financial Aid 2026","category":"Scholarships",
     "description":"Merit, need-based, government and external scholarship programmes",
     "file_url":f"{_KB_BASE}/Scholarships_Financial_Aid_2026.pdf","file_name":"Scholarships_Financial_Aid_2026.pdf",
     "uploaded_by":"dev-admin","status":"indexed","chunk_count":32,
     "created_at":"2026-07-01T10:05:00Z","updated_at":"2026-07-01T10:05:00Z"},
    {"id":"doc-007","title":"Course Catalog & Programmes","category":"Academics",
     "description":"Detailed curriculum for all UG and PG programmes 2026-27",
     "file_url":f"{_KB_BASE}/Course_Catalog_and_Programs.pdf","file_name":"Course_Catalog_and_Programs.pdf",
     "uploaded_by":"dev-admin","status":"indexed","chunk_count":40,
     "created_at":"2026-07-01T10:06:00Z","updated_at":"2026-07-01T10:06:00Z"},
    {"id":"doc-008","title":"Academic Calendar 2026-27","category":"Academics",
     "description":"Official schedule: classes, exams, holidays and events",
     "file_url":f"{_KB_BASE}/Academic_Calendar_2026.pdf","file_name":"Academic_Calendar_2026.pdf",
     "uploaded_by":"dev-admin","status":"indexed","chunk_count":22,
     "created_at":"2026-07-01T10:07:00Z","updated_at":"2026-07-01T10:07:00Z"},
    {"id":"doc-009","title":"Library Guide 2026","category":"Library",
     "description":"Central library services, collections, borrowing rules and digital resources",
     "file_url":f"{_KB_BASE}/Library_Guide_2026.pdf","file_name":"Library_Guide_2026.pdf",
     "uploaded_by":"dev-admin","status":"indexed","chunk_count":30,
     "created_at":"2026-07-01T10:08:00Z","updated_at":"2026-07-01T10:08:00Z"},
    {"id":"doc-010","title":"Transport Guide 2026","category":"Transport",
     "description":"University bus routes, timings, fees and conduct policy",
     "file_url":f"{_KB_BASE}/Transport_Guide_2026.pdf","file_name":"Transport_Guide_2026.pdf",
     "uploaded_by":"dev-admin","status":"indexed","chunk_count":28,
     "created_at":"2026-07-01T10:09:00Z","updated_at":"2026-07-01T10:09:00Z"},
    {"id":"doc-011","title":"Research & Innovation Handbook","category":"Research",
     "description":"PhD programme, research centres, patents and startup incubation",
     "file_url":f"{_KB_BASE}/Research_Innovation_Handbook.pdf","file_name":"Research_Innovation_Handbook.pdf",
     "uploaded_by":"dev-admin","status":"indexed","chunk_count":34,
     "created_at":"2026-07-01T10:10:00Z","updated_at":"2026-07-01T10:10:00Z"},
    {"id":"doc-012","title":"Department Handbook: CSE","category":"Departments",
     "description":"CSE faculty directory, labs, research groups and student clubs",
     "file_url":f"{_KB_BASE}/Department_Handbook_CSE.pdf","file_name":"Department_Handbook_CSE.pdf",
     "uploaded_by":"dev-admin","status":"indexed","chunk_count":30,
     "created_at":"2026-07-01T10:11:00Z","updated_at":"2026-07-01T10:11:00Z"},
    {"id":"doc-013","title":"Student Handbook & Code of Conduct","category":"General",
     "description":"Student rights, responsibilities, anti-ragging and wellness services",
     "file_url":f"{_KB_BASE}/Student_Handbook_Code_of_Conduct.pdf","file_name":"Student_Handbook_Code_of_Conduct.pdf",
     "uploaded_by":"dev-admin","status":"indexed","chunk_count":36,
     "created_at":"2026-07-01T10:12:00Z","updated_at":"2026-07-01T10:12:00Z"},
    {"id":"doc-014","title":"Campus Facilities Guide","category":"Campus",
     "description":"Sports, cafeteria, IT infrastructure and health centre",
     "file_url":f"{_KB_BASE}/Campus_Facilities_Guide.pdf","file_name":"Campus_Facilities_Guide.pdf",
     "uploaded_by":"dev-admin","status":"indexed","chunk_count":28,
     "created_at":"2026-07-01T10:13:00Z","updated_at":"2026-07-01T10:13:00Z"},
    {"id":"doc-015","title":"International Exchange Programme","category":"International",
     "description":"Partner universities, application process and exchange scholarships",
     "file_url":f"{_KB_BASE}/International_Exchange_Programme.pdf","file_name":"International_Exchange_Programme.pdf",
     "uploaded_by":"dev-admin","status":"uploaded","chunk_count":0,
     "created_at":"2026-07-01T10:14:00Z","updated_at":"2026-07-01T10:14:00Z"},
    {"id":"doc-016","title":"Industry Interface & MoU Directory","category":"Industry",
     "description":"Corporate partners, MoUs and Centres of Excellence",
     "file_url":f"{_KB_BASE}/Industry_Interface_MoU_Directory.pdf","file_name":"Industry_Interface_MoU_Directory.pdf",
     "uploaded_by":"dev-admin","status":"uploaded","chunk_count":0,
     "created_at":"2026-07-01T10:15:00Z","updated_at":"2026-07-01T10:15:00Z"},
    {"id":"doc-017","title":"NSS, NCC & Social Outreach Handbook","category":"Campus",
     "description":"National Service Scheme, NCC wing and social outreach programmes",
     "file_url":f"{_KB_BASE}/NSS_NCC_Social_Outreach.pdf","file_name":"NSS_NCC_Social_Outreach.pdf",
     "uploaded_by":"dev-admin","status":"uploaded","chunk_count":0,
     "created_at":"2026-07-01T10:16:00Z","updated_at":"2026-07-01T10:16:00Z"},
]


class DocumentService:
    """Service handling document management, upload, storage, and RAG ingestion."""

    @staticmethod
    def list_documents(category: Optional[str] = None, status: Optional[str] = None) -> DocumentListResponse:
        supabase = get_supabase_client()
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"

        if not is_placeholder:
            try:
                query = supabase.table("documents").select("*")
                if category:
                    query = query.eq("category", category)
                if status:
                    query = query.eq("status", status)
                res = query.order("created_at", desc=True).execute()
                docs = [DocumentOut(**doc) for doc in res.data]
                return DocumentListResponse(
                    message="Documents fetched successfully",
                    status="success",
                    count=len(docs),
                    documents=docs,
                )
            except Exception:
                pass

        filtered = MOCK_DOCUMENTS
        if category:
            filtered = [d for d in filtered if d["category"].lower() == category.lower()]
        if status:
            filtered = [d for d in filtered if d["status"].lower() == status.lower()]

        docs = [DocumentOut(**d) for d in filtered]
        return DocumentListResponse(
            message="Documents fetched successfully (Development Mode)",
            status="success",
            count=len(docs),
            documents=docs,
        )

    @staticmethod
    def get_document(document_id: str) -> DocumentResponse:
        supabase = get_supabase_client()
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"

        if not is_placeholder:
            try:
                res = supabase.table("documents").select("*").eq("id", document_id).single().execute()
                if res.data:
                    return DocumentResponse(
                        message="Document details fetched successfully",
                        status="success",
                        data=DocumentOut(**res.data),
                    )
            except Exception:
                pass

        match = next((d for d in MOCK_DOCUMENTS if d["id"] == document_id), None)
        if match:
            return DocumentResponse(
                message="Document details fetched successfully (Dev)",
                status="success",
                data=DocumentOut(**match),
            )
        return DocumentResponse(message=f"Document with ID {document_id} not found", status="error")

    @staticmethod
    def upload_and_process_pdf(
        file_bytes: bytes,
        filename: str,
        title: str,
        category: str,
        description: Optional[str],
        uploaded_by: Optional[str],
        background_tasks: BackgroundTasks
    ) -> DocumentResponse:
        """
        Uploads PDF to Supabase Storage bucket 'documents', inserts database record with status 'uploaded',
        and schedules background PDF processing task (extract -> clean -> chunk -> BAAI embeddings -> Pinecone).
        """
        # Step 1: Validate PDF input
        validate_pdf_file(file_bytes, filename)

        supabase = get_supabase_client()
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"
        document_id = str(uuid.uuid4())
        safe_filename = f"{document_id}_{filename.replace(' ', '_')}"
        file_path = f"pdfs/{safe_filename}"
        public_url = f"{settings.supabase_url}/storage/v1/object/public/documents/{file_path}"

        # Step 2: Upload file to Supabase Storage bucket 'documents'
        if not is_placeholder:
            try:
                supabase.storage.from_("documents").upload(
                    path=file_path,
                    file=file_bytes,
                    file_options={"content-type": "application/pdf", "upsert": "true"}
                )
            except Exception as err:
                print(f"Storage upload note: {err}")

        # Step 3: Insert DB record with status 'uploaded'
        data_to_insert = {
            "id": document_id,
            "title": title,
            "category": category,
            "description": description,
            "file_url": public_url,
            "file_name": safe_filename,
            "uploaded_by": uploaded_by,
            "status": "uploaded",
        }

        if not is_placeholder:
            try:
                res = supabase.table("documents").insert(data_to_insert).execute()
                doc_record = res.data[0] if res.data else data_to_insert
            except Exception as insert_err:
                print(f"Database document insert note: {insert_err}")
                doc_record = data_to_insert
        else:
            doc_record = {
                **data_to_insert,
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }
            MOCK_DOCUMENTS.append(doc_record)

        # Step 4: Schedule non-blocking background processing task
        background_tasks.add_task(
            process_and_index_document,
            document_id=document_id,
            file_bytes=file_bytes,
            title=title,
            category=category,
            filename=filename
        )

        return DocumentResponse(
            message="PDF uploaded successfully. Processing started in background.",
            status="success",
            data=DocumentOut(**doc_record)
        )

    @staticmethod
    def update_document(document_id: str, payload: DocumentUpdate) -> DocumentResponse:
        supabase = get_supabase_client()
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"

        updates = {k: v for k, v in payload.model_dump().items() if v is not None}

        if not is_placeholder:
            try:
                res = supabase.table("documents").update(updates).eq("id", document_id).execute()
                if res.data and len(res.data) > 0:
                    return DocumentResponse(
                        message="Document updated successfully",
                        status="success",
                        data=DocumentOut(**res.data[0]),
                    )
            except Exception as err:
                if settings.environment != "development":
                    raise err

        match = next((d for d in MOCK_DOCUMENTS if d["id"] == document_id), None)
        if match:
            match.update(updates)
            return DocumentResponse(
                message="Document updated successfully (Dev)",
                status="success",
                data=DocumentOut(**match),
            )
        return DocumentResponse(message=f"Document {document_id} not found", status="error")

    @staticmethod
    def delete_document(document_id: str) -> DocumentResponse:
        """
        Complete document deletion:
        Removes PDF file from Supabase Storage, deletes Pinecone vectors, and deletes DB row.
        """
        supabase = get_supabase_client()
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"

        file_path = None
        if not is_placeholder:
            try:
                res = supabase.table("documents").select("file_name").eq("id", document_id).single().execute()
                if res.data and res.data.get("file_name"):
                    file_path = f"pdfs/{res.data['file_name']}"
            except Exception:
                pass

        # Execute 3-step deletion
        success = delete_document_completely(document_id=document_id, file_path=file_path)

        global MOCK_DOCUMENTS
        MOCK_DOCUMENTS = [d for d in MOCK_DOCUMENTS if d["id"] != document_id]

        if success:
            return DocumentResponse(message=f"Document {document_id} and related vectors deleted successfully", status="success")
        return DocumentResponse(message=f"Document {document_id} removed", status="success")

    @staticmethod
    def create_document(payload: DocumentCreate, uploaded_by: Optional[str] = None) -> DocumentResponse:
        supabase = get_supabase_client()
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"
        document_id = str(uuid.uuid4())
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        data = {
            "id": document_id,
            "title": payload.title,
            "category": payload.category,
            "description": payload.description,
            "file_url": payload.file_url,
            "file_name": payload.file_name,
            "uploaded_by": uploaded_by,
            "status": payload.status,
            "created_at": now_iso,
            "updated_at": now_iso,
        }
        if not is_placeholder:
            try:
                res = supabase.table("documents").insert(data).execute()
                if res.data:
                    return DocumentResponse(message="Document created successfully", status="success", data=DocumentOut(**res.data[0]))
            except Exception as err:
                logger.error(f"Document create error: {err}")
        MOCK_DOCUMENTS.append(data)
        return DocumentResponse(message="Document created successfully", status="success", data=DocumentOut(**data))

    @staticmethod
    def reprocess_document(document_id: str, background_tasks: BackgroundTasks) -> DocumentResponse:
        """
        Re-run full RAG pipeline on an existing document.
        Fetches the PDF bytes from Supabase Storage and reprocesses through
        extract → chunk → embed → Pinecone upsert.
        """
        supabase = get_supabase_client()
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"

        if is_placeholder:
            return DocumentResponse(
                message="Reprocess not available in dev mode (no real Supabase Storage).",
                status="error",
            )

        try:
            # 1. Fetch document record
            res = supabase.table("documents").select("*").eq("id", document_id).single().execute()
            if not res.data:
                raise HTTPException(status_code=404, detail=f"Document {document_id} not found.")
            doc = res.data
            file_name = doc.get("file_name", "")
            title = doc.get("title", "Document")
            category = doc.get("category", "General")
            file_path = f"pdfs/{file_name}"

            # 2. Download PDF bytes from Supabase Storage
            file_bytes = supabase.storage.from_("documents").download(file_path)
            if not file_bytes:
                raise HTTPException(status_code=404, detail="PDF file not found in storage.")

            # 3. Set status to 'uploaded' so it goes through processing again
            supabase.table("documents").update({"status": "uploaded"}).eq("id", document_id).execute()

            # 4. Schedule background reprocessing
            background_tasks.add_task(
                process_and_index_document,
                document_id=document_id,
                file_bytes=file_bytes,
                title=title,
                category=category,
                filename=file_name,
            )

            return DocumentResponse(
                message="Reprocessing started. Document will be re-indexed shortly.",
                status="success",
                data=DocumentOut(**{**doc, "status": "uploaded"}),
            )
        except HTTPException:
            raise
        except Exception as err:
            logger.error(f"Reprocess error for {document_id}: {err}")
            raise HTTPException(status_code=500, detail=f"Reprocess failed: {str(err)}")

