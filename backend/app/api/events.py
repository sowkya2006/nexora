from fastapi import APIRouter, Depends, Query
from typing import Optional

from app.auth.dependencies import get_current_admin
from app.schemas.api import EventCreate, EventUpdate, EventResponse, EventListResponse
from app.schemas.auth import AdminUser
from app.services.event_service import EventService

router = APIRouter()


@router.get("/", response_model=EventListResponse)
async def list_events(
    status: Optional[str] = Query(None, description="Filter by status (upcoming/active/completed/archived)"),
):
    """List all university events with optional status filter."""
    return EventService.list_events(status=status)


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: str):
    """Get a single event by ID."""
    return EventService.get_event(event_id)


@router.post("/", response_model=EventResponse)
async def create_event(
    payload: EventCreate,
    admin: AdminUser = Depends(get_current_admin),
):
    """Create a new event (Admin only)."""
    return EventService.create_event(payload, created_by=admin.id)


@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: str,
    payload: EventUpdate,
    _admin: AdminUser = Depends(get_current_admin),
):
    """Update an existing event (Admin only)."""
    return EventService.update_event(event_id, payload)


@router.delete("/{event_id}", response_model=EventResponse)
async def delete_event(
    event_id: str,
    _admin: AdminUser = Depends(get_current_admin),
):
    """Delete an event (Admin only)."""
    return EventService.delete_event(event_id)
