from fastapi import APIRouter, Depends, Query
from typing import Optional

from app.auth.dependencies import get_current_admin
from app.schemas.api import NoticeCreate, NoticeUpdate, NoticeResponse, NoticeListResponse
from app.schemas.auth import AdminUser
from app.services.notice_service import NoticeService

router = APIRouter()


@router.get("/", response_model=NoticeListResponse)
async def list_notices(
    category: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status (draft/published/archived)"),
):
    """List all university notices with optional category and status filters."""
    return NoticeService.list_notices(category=category, status=status)


@router.get("/{notice_id}", response_model=NoticeResponse)
async def get_notice(notice_id: str):
    """Get a single notice by ID."""
    return NoticeService.get_notice(notice_id)


@router.post("/", response_model=NoticeResponse)
async def create_notice(
    payload: NoticeCreate,
    admin: AdminUser = Depends(get_current_admin),
):
    """Create a new university notice (Admin only)."""
    return NoticeService.create_notice(payload, created_by=admin.id)


@router.put("/{notice_id}", response_model=NoticeResponse)
async def update_notice(
    notice_id: str,
    payload: NoticeUpdate,
    _admin: AdminUser = Depends(get_current_admin),
):
    """Update an existing notice (Admin only)."""
    return NoticeService.update_notice(notice_id, payload)


@router.delete("/{notice_id}", response_model=NoticeResponse)
async def delete_notice(
    notice_id: str,
    _admin: AdminUser = Depends(get_current_admin),
):
    """Delete a notice (Admin only)."""
    return NoticeService.delete_notice(notice_id)
