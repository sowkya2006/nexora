from fastapi import APIRouter

from app.api import analytics, auth, chat, documents, events, notices, settings, admin_tools

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(notices.router, prefix="/notices", tags=["notices"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(admin_tools.router, tags=["admin-tools"])
