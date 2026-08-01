from functools import lru_cache
from pinecone import Pinecone
from app.config import settings

_pc: Pinecone | None = None


@lru_cache
def get_pinecone_client() -> Pinecone:
    """Returns a cached Pinecone client instance."""
    global _pc
    if _pc is None:
        _pc = Pinecone(api_key=settings.pinecone_api_key.strip())
    return _pc


def get_pinecone_index():
    """
    Returns the configured Pinecone index.
    Strips all whitespace from host and index name to handle
    accidental tabs or spaces from environment variable editors.
    """
    client = get_pinecone_client()
    host = settings.pinecone_host.strip()
    index_name = settings.pinecone_index_name.strip()

    if host:
        return client.Index(host=host)
    return client.Index(index_name)
