import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    description="Backend API for Nexora University – UniSphere AI",
    version=settings.app_version,
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url="/redoc" if settings.environment != "production" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount knowledge_base directory for serving PDFs via /knowledge_base/<filename>
kb_dir = Path(__file__).parent.parent.parent / "knowledge_base"
if kb_dir.exists():
    app.mount("/knowledge_base", StaticFiles(directory=str(kb_dir)), name="knowledge_base")

app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/health", tags=["health"])
async def health_check():
    """Root health check endpoint."""
    is_configured = settings.supabase_url != "https://your-project.supabase.co"
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "supabase_configured": is_configured,
        "pinecone_configured": settings.pinecone_api_key != "your-pinecone-api-key",
        "groq_configured": settings.groq_api_key != "your-groq-api-key",
        "pinecone_index": settings.pinecone_index_name.strip(),
        "pinecone_host_set": bool(settings.pinecone_host.strip()),
        "pinecone_host_prefix": settings.pinecone_host.strip()[:40] if settings.pinecone_host.strip() else "NOT SET",
    }

