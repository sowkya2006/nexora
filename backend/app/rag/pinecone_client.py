from functools import lru_cache
from pinecone import Pinecone
from app.config import settings

_pc: Pinecone | None = None


@lru_cache
def get_pinecone_client() -> Pinecone:
    """Returns a cached Pinecone client instance."""
    global _pc
    if _pc is None:
        _pc = Pinecone(api_key=settings.pinecone_api_key)
    return _pc


def get_pinecone_index():
    """
    Returns the configured Pinecone index.
    Uses pinecone_host if set (required for serverless indexes),
    otherwise uses the index name directly (for pod-based indexes).
    """
    client = get_pinecone_client()
    host = getattr(settings, "pinecone_host", None)
    if host and host.strip():
        return client.Index(host=host)
    return client.Index(settings.pinecone_index_name)
