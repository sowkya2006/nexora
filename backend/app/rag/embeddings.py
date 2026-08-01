import logging
from functools import lru_cache
from typing import List
from sentence_transformers import SentenceTransformer
from app.config import settings

logger = logging.getLogger(__name__)

_model_instance: SentenceTransformer | None = None


def load_embedding_model() -> SentenceTransformer:
    """
    Loads the BAAI/bge-large-en-v1.5 embedding model once into memory.
    Reused across all document processing and query embedding tasks.
    """
    global _model_instance
    if _model_instance is None:
        logger.info(f"Loading embedding model '{settings.embedding_model}'...")
        _model_instance = SentenceTransformer(
            settings.embedding_model,
            device="cpu"
        )
        logger.info("Embedding model loaded successfully!")
    return _model_instance


@lru_cache
def get_embeddings_model() -> SentenceTransformer:
    """Returns the cached singleton embedding model instance."""
    return load_embedding_model()


def generate_chunk_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates 1024-dimensional normalized vector embeddings for a list of text chunks.
    """
    model = get_embeddings_model()
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False
    )
    return embeddings.tolist()
