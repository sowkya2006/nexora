from fastapi import APIRouter, Depends, Query
from typing import Optional

from app.auth.dependencies import get_current_admin
from app.schemas.api import AnalyticsResponse
from app.schemas.auth import AdminUser
from app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/overview", response_model=AnalyticsResponse)
async def get_analytics_overview(
    _admin: AdminUser = Depends(get_current_admin),
):
    """Dashboard analytics overview — total documents, notices, events, chats, chunks."""
    return AnalyticsService.get_overview()


@router.get("/ai", response_model=AnalyticsResponse)
async def get_ai_analytics(
    _admin: AdminUser = Depends(get_current_admin),
):
    """AI chatbot analytics — total queries, recent searches, top intents, confidence."""
    return AnalyticsService.get_ai_analytics()


@router.get("/documents", response_model=AnalyticsResponse)
async def get_document_analytics(
    _admin: AdminUser = Depends(get_current_admin),
):
    """Document analytics — counts by status and category, total chunks."""
    return AnalyticsService.get_document_analytics()


@router.post("/event", response_model=AnalyticsResponse)
async def log_analytics_event(
    event_type: str = Query(..., description="Event type (e.g. page_view, document_download, chat_query)"),
    document_id: Optional[str] = Query(None, description="Optional associated document ID"),
    page_name: Optional[str] = Query(None, description="Optional page name"),
):
    """Record an analytics event (public — no auth required)."""
    return AnalyticsService.log_event(event_type=event_type, document_id=document_id, page_name=page_name)
