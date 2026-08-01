from typing import List, Optional
from app.config import settings
from app.database.supabase import get_supabase_client
from app.schemas.api import NoticeCreate, NoticeUpdate, NoticeOut, NoticeListResponse, NoticeResponse

MOCK_NOTICES = [
    {
        "id": "not-001",
        "title": "Spring Semester 2026 Registration Announcement",
        "description": "Course registration for Spring Semester 2026 opens on February 10th.",
        "category": "Academic",
        "attachment_url": "/notices/spring_registration_2026.pdf",
        "status": "published",
        "published_at": "2026-01-20T09:00:00Z",
        "created_by": "dev-admin-0000-0000-000000000000",
        "created_at": "2026-01-20T09:00:00Z",
        "updated_at": "2026-01-20T09:00:00Z",
    },
    {
        "id": "not-002",
        "title": "Mid-Term Examination Schedule",
        "description": "Mid-term examination timetable for B.Tech and M.Tech programs.",
        "category": "Examination",
        "attachment_url": "/notices/midterm_timetable.pdf",
        "status": "published",
        "published_at": "2026-01-25T11:00:00Z",
        "created_by": "dev-admin-0000-0000-000000000000",
        "created_at": "2026-01-25T11:00:00Z",
        "updated_at": "2026-01-25T11:00:00Z",
    },
]


class NoticeService:
    """Service handling notice management and database operations."""

    @staticmethod
    def list_notices(category: Optional[str] = None, status: Optional[str] = None) -> NoticeListResponse:
        supabase = get_supabase_client()
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"

        if not is_placeholder:
            try:
                query = supabase.table("notices").select("*")
                if category:
                    query = query.eq("category", category)
                if status:
                    query = query.eq("status", status)
                res = query.order("created_at", desc=True).execute()
                notices = [NoticeOut(**n) for n in res.data]
                return NoticeListResponse(
                    message="Notices fetched successfully",
                    status="success",
                    count=len(notices),
                    notices=notices,
                )
            except Exception:
                pass

        # Dev Fallback Mode
        filtered = MOCK_NOTICES
        if category:
            filtered = [n for n in filtered if n["category"].lower() == category.lower()]
        if status:
            filtered = [n for n in filtered if n["status"].lower() == status.lower()]

        notices = [NoticeOut(**n) for n in filtered]
        return NoticeListResponse(
            message="Notices fetched successfully (Development Mode)",
            status="success",
            count=len(notices),
            notices=notices,
        )

    @staticmethod
    def get_notice(notice_id: str) -> NoticeResponse:
        supabase = get_supabase_client()
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"

        if not is_placeholder:
            try:
                res = supabase.table("notices").select("*").eq("id", notice_id).single().execute()
                if res.data:
                    return NoticeResponse(
                        message="Notice fetched successfully",
                        status="success",
                        data=NoticeOut(**res.data),
                    )
            except Exception:
                pass

        match = next((n for n in MOCK_NOTICES if n["id"] == notice_id), None)
        if match:
            return NoticeResponse(
                message="Notice fetched successfully (Dev)",
                status="success",
                data=NoticeOut(**match),
            )
        return NoticeResponse(message=f"Notice with ID {notice_id} not found", status="error")

    @staticmethod
    def create_notice(payload: NoticeCreate, created_by: Optional[str] = None) -> NoticeResponse:
        supabase = get_supabase_client()
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"

        data_to_insert = {
            "title": payload.title,
            "description": payload.description,
            "category": payload.category,
            "attachment_url": payload.attachment_url,
            "status": payload.status,
            "created_by": created_by,
        }

        if not is_placeholder:
            try:
                res = supabase.table("notices").insert(data_to_insert).execute()
                if res.data and len(res.data) > 0:
                    return NoticeResponse(
                        message="Notice created successfully",
                        status="success",
                        data=NoticeOut(**res.data[0]),
                    )
            except Exception as err:
                if settings.environment != "development":
                    raise err

        new_notice = {
            "id": f"not-{len(MOCK_NOTICES) + 1:03d}",
            **data_to_insert,
            "published_at": "2026-07-30T10:00:00Z" if payload.status == "published" else None,
            "created_at": "2026-07-30T10:00:00Z",
            "updated_at": "2026-07-30T10:00:00Z",
        }
        MOCK_NOTICES.append(new_notice)
        return NoticeResponse(
            message="Notice created successfully (Dev Mode)",
            status="success",
            data=NoticeOut(**new_notice),
        )

    @staticmethod
    def update_notice(notice_id: str, payload: NoticeUpdate) -> NoticeResponse:
        supabase = get_supabase_client()
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"

        updates = {k: v for k, v in payload.model_dump().items() if v is not None}

        if not is_placeholder:
            try:
                res = supabase.table("notices").update(updates).eq("id", notice_id).execute()
                if res.data and len(res.data) > 0:
                    return NoticeResponse(
                        message="Notice updated successfully",
                        status="success",
                        data=NoticeOut(**res.data[0]),
                    )
            except Exception as err:
                if settings.environment != "development":
                    raise err

        match = next((n for n in MOCK_NOTICES if n["id"] == notice_id), None)
        if match:
            match.update(updates)
            return NoticeResponse(
                message="Notice updated successfully (Dev)",
                status="success",
                data=NoticeOut(**match),
            )
        return NoticeResponse(message=f"Notice {notice_id} not found", status="error")

    @staticmethod
    def delete_notice(notice_id: str) -> NoticeResponse:
        supabase = get_supabase_client()
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"

        if not is_placeholder:
            try:
                supabase.table("notices").delete().eq("id", notice_id).execute()
                return NoticeResponse(message=f"Notice {notice_id} deleted successfully", status="success")
            except Exception as err:
                if settings.environment != "development":
                    raise err

        global MOCK_NOTICES
        MOCK_NOTICES = [n for n in MOCK_NOTICES if n["id"] != notice_id]
        return NoticeResponse(message=f"Notice {notice_id} deleted successfully (Dev)", status="success")
