from pydantic import BaseModel, Field
from typing import Optional, List, Any


# --- Chat Schemas ---
class ChatRequest(BaseModel):
    message: str
    session_id: str
    history: List[dict] = []


class ChatSource(BaseModel):
    document_name: str
    page: Optional[int] = None
    document_id: Optional[str] = None


class ChatResponse(BaseModel):
    message: str
    status: str = "success"
    session_id: Optional[str] = None
    sources: List[ChatSource] = []


class ChatQueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
    history: List[dict] = []


class SourceReference(BaseModel):
    document: str
    page: int
    snippet: str


class ChatQueryResponse(BaseModel):
    answer: str
    sources: List[SourceReference] = []
    confidence_score: float = 0.0



# --- Document Schemas ---
class DocumentCreate(BaseModel):
    title: str
    category: str
    description: Optional[str] = None
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    status: str = "uploaded"


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    status: Optional[str] = None


class DocumentOut(BaseModel):
    id: str
    title: str
    category: str
    description: Optional[str] = None
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    uploaded_by: Optional[str] = None
    status: str = "uploaded"
    chunk_count: Optional[int] = 0
    processed_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class DocumentResponse(BaseModel):
    message: str
    status: str = "success"
    data: Optional[Any] = None


class DocumentListResponse(BaseModel):
    message: str
    status: str = "success"
    count: int = 0
    documents: List[DocumentOut] = []


# --- Notice Schemas ---
class NoticeCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = "Academic"
    attachment_url: Optional[str] = None
    status: str = "draft"


class NoticeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    attachment_url: Optional[str] = None
    status: Optional[str] = None


class NoticeOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    attachment_url: Optional[str] = None
    status: str = "draft"
    published_at: Optional[str] = None
    created_by: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class NoticeResponse(BaseModel):
    message: str
    status: str = "success"
    data: Optional[Any] = None


class NoticeListResponse(BaseModel):
    message: str
    status: str = "success"
    count: int = 0
    notices: List[NoticeOut] = []


# --- Event Schemas ---
class EventCreate(BaseModel):
    name: str
    description: Optional[str] = None
    date: str
    venue: Optional[str] = None
    organizer: Optional[str] = None
    brochure_url: Optional[str] = None
    status: str = "upcoming"


class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None
    venue: Optional[str] = None
    organizer: Optional[str] = None
    brochure_url: Optional[str] = None
    status: Optional[str] = None


class EventOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    date: str
    venue: Optional[str] = None
    organizer: Optional[str] = None
    brochure_url: Optional[str] = None
    status: str = "upcoming"
    created_by: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class EventResponse(BaseModel):
    message: str
    status: str = "success"
    data: Optional[Any] = None


class EventListResponse(BaseModel):
    message: str
    status: str = "success"
    count: int = 0
    events: List[EventOut] = []


# --- Settings Schemas ---
class SettingsUpdate(BaseModel):
    name: Optional[str] = None
    tagline: Optional[str] = None
    description: Optional[str] = None
    vision: Optional[str] = None
    mission: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    social_links: Optional[dict] = None


class SettingsOut(BaseModel):
    id: Optional[str] = None
    name: str = "Nexora University"
    tagline: Optional[str] = None
    description: Optional[str] = None
    vision: Optional[str] = None
    mission: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    social_links: Optional[dict] = Field(default_factory=dict)
    updated_at: Optional[str] = None


class SettingsResponse(BaseModel):
    message: str
    status: str = "success"
    data: Optional[SettingsOut] = None


# --- Analytics Schemas ---
class AnalyticsOverviewOut(BaseModel):
    total_documents: int = 0
    total_notices: int = 0
    total_events: int = 0
    total_chats: int = 0
    total_chunks: int = 0
    recent_activity: List[dict] = []


class AnalyticsResponse(BaseModel):
    message: str
    status: str = "success"
    data: Optional[Any] = None
