from typing import List, Optional
from app.config import settings
from app.database.supabase import get_supabase_client
from app.schemas.api import EventCreate, EventUpdate, EventOut, EventListResponse, EventResponse

MOCK_EVENTS = [
    {
        "id": "evt-001",
        "name": "Annual Tech Symposium 2026",
        "description": "National level tech festival showcasing innovative projects, hackathons, and guest lectures.",
        "date": "2026-03-15",
        "venue": "Main Auditorium & Convention Center",
        "organizer": "Department of Computer Science & Engineering",
        "brochure_url": "/events/tech_symposium_2026.pdf",
        "status": "upcoming",
        "created_by": "dev-admin-0000-0000-000000000000",
        "created_at": "2026-01-10T10:00:00Z",
        "updated_at": "2026-01-10T10:00:00Z",
    },
    {
        "id": "evt-002",
        "name": "Global Career & Placement Expo 2026",
        "description": "Meet recruiters from 100+ global enterprises and startups.",
        "date": "2026-04-02",
        "venue": "Campus Sports Complex",
        "organizer": "Placement & Career Development Cell",
        "brochure_url": "/events/placement_expo_2026.pdf",
        "status": "upcoming",
        "created_by": "dev-admin-0000-0000-000000000000",
        "created_at": "2026-01-12T10:00:00Z",
        "updated_at": "2026-01-12T10:00:00Z",
    },
]


class EventService:
    """Service handling event management and database operations."""

    @staticmethod
    def list_events(status: Optional[str] = None) -> EventListResponse:
        supabase = get_supabase_client()
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"

        if not is_placeholder:
            try:
                query = supabase.table("events").select("*")
                if status:
                    query = query.eq("status", status)
                res = query.order("date", desc=False).execute()
                events = [EventOut(**e) for e in res.data]
                return EventListResponse(
                    message="Events fetched successfully",
                    status="success",
                    count=len(events),
                    events=events,
                )
            except Exception:
                pass

        filtered = MOCK_EVENTS
        if status:
            filtered = [e for e in filtered if e["status"].lower() == status.lower()]

        events = [EventOut(**e) for e in filtered]
        return EventListResponse(
            message="Events fetched successfully (Development Mode)",
            status="success",
            count=len(events),
            events=events,
        )

    @staticmethod
    def get_event(event_id: str) -> EventResponse:
        supabase = get_supabase_client()
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"

        if not is_placeholder:
            try:
                res = supabase.table("events").select("*").eq("id", event_id).single().execute()
                if res.data:
                    return EventResponse(
                        message="Event fetched successfully",
                        status="success",
                        data=EventOut(**res.data),
                    )
            except Exception:
                pass

        match = next((e for e in MOCK_EVENTS if e["id"] == event_id), None)
        if match:
            return EventResponse(
                message="Event fetched successfully (Dev)",
                status="success",
                data=EventOut(**match),
            )
        return EventResponse(message=f"Event with ID {event_id} not found", status="error")

    @staticmethod
    def create_event(payload: EventCreate, created_by: Optional[str] = None) -> EventResponse:
        supabase = get_supabase_client()
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"

        data_to_insert = {
            "name": payload.name,
            "description": payload.description,
            "date": payload.date,
            "venue": payload.venue,
            "organizer": payload.organizer,
            "brochure_url": payload.brochure_url,
            "status": payload.status,
            "created_by": created_by,
        }

        if not is_placeholder:
            try:
                res = supabase.table("events").insert(data_to_insert).execute()
                if res.data and len(res.data) > 0:
                    return EventResponse(
                        message="Event created successfully",
                        status="success",
                        data=EventOut(**res.data[0]),
                    )
            except Exception as err:
                if settings.environment != "development":
                    raise err

        new_event = {
            "id": f"evt-{len(MOCK_EVENTS) + 1:03d}",
            **data_to_insert,
            "created_at": "2026-07-30T10:00:00Z",
            "updated_at": "2026-07-30T10:00:00Z",
        }
        MOCK_EVENTS.append(new_event)
        return EventResponse(
            message="Event created successfully (Dev Mode)",
            status="success",
            data=EventOut(**new_event),
        )

    @staticmethod
    def update_event(event_id: str, payload: EventUpdate) -> EventResponse:
        supabase = get_supabase_client()
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"

        updates = {k: v for k, v in payload.model_dump().items() if v is not None}

        if not is_placeholder:
            try:
                res = supabase.table("events").update(updates).eq("id", event_id).execute()
                if res.data and len(res.data) > 0:
                    return EventResponse(
                        message="Event updated successfully",
                        status="success",
                        data=EventOut(**res.data[0]),
                    )
            except Exception as err:
                if settings.environment != "development":
                    raise err

        match = next((e for e in MOCK_EVENTS if e["id"] == event_id), None)
        if match:
            match.update(updates)
            return EventResponse(
                message="Event updated successfully (Dev)",
                status="success",
                data=EventOut(**match),
            )
        return EventResponse(message=f"Event {event_id} not found", status="error")

    @staticmethod
    def delete_event(event_id: str) -> EventResponse:
        supabase = get_supabase_client()
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"

        if not is_placeholder:
            try:
                supabase.table("events").delete().eq("id", event_id).execute()
                return EventResponse(message=f"Event {event_id} deleted successfully", status="success")
            except Exception as err:
                if settings.environment != "development":
                    raise err

        global MOCK_EVENTS
        MOCK_EVENTS = [e for e in MOCK_EVENTS if e["id"] != event_id]
        return EventResponse(message=f"Event {event_id} deleted successfully (Dev)", status="success")
