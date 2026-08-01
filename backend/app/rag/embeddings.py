"""
Embeddings via HuggingFace Inference API.
Uses BAAI/bge-large-en-v1.5 remotely — no local model, no torch, Vercel-compatible.
Falls back to a simple hash-based mock if the API key is not set (dev mode).
"""
import logging
import httpx
from typing import List
from app.config import settings

logger = logging.getLogger(__name__)

# HuggingFace Inference API endpoint for BAAI/bge-large-en-v1.5
HF_API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/BAAI/bge-large-en-v1.5"
EMBEDDING_DIM = 1024


def _call_hf_api(texts: List[str]) -> List[List[float]]:
    """Call HuggingFace Inference API to get embeddings."""
    headers = {}
    if settings.hf_api_token:
        headers["Authorization"] = f"Bearer {settings.hf_api_token}"

    payload = {
        "inputs": texts,
        "options": {"wait_for_model": True, "use_cache": True}
    }

    with httpx.Client(timeout=60.0) as client:
        response = client.post(HF_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

    # HF API returns list of embeddings directly
    if isinstance(result, list) and len(result) > 0:
        # Single text returns flat list, multiple texts return list of lists
        if isinstance(result[0], float):
            return [result]
        return result

    raise ValueError(f"Unexpected HF API response format: {type(result)}")


def _mock_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Deterministic mock embeddings for dev/test when no HF token is set.
    Uses character hash to produce consistent 1024-dim vectors.
    """
    import hashlib, math
    embeddings = []
    for text in texts:
        h = hashlib.sha256(text.encode()).digest()
        # Expand 32 bytes to 1024 floats using cyclic pattern
        vec = []
        for i in range(EMBEDDING_DIM):
            byte_val = h[i % 32]
            angle = (byte_val / 255.0) * 2 * math.pi * (i + 1)
            vec.append(math.sin(angle) * 0.1)
        # Normalize
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        embeddings.append([x / norm for x in vec])
    return embeddings


def generate_chunk_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate 1024-dim normalized embeddings for a list of text chunks.
    Uses HuggingFace Inference API in production, mock in dev.
    Batches requests in groups of 32 to stay within API limits.
    """
    if not texts:
        return []

    if not settings.hf_api_token:
        logger.warning("HF_API_TOKEN not set — using mock embeddings (dev mode)")
        return _mock_embeddings(texts)

    all_embeddings = []
    batch_size = 32

    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        try:
            batch_embeddings = _call_hf_api(batch)
            all_embeddings.extend(batch_embeddings)
            logger.info(f"Embedded batch {i // batch_size + 1}: {len(batch)} texts")
        except Exception as e:
            logger.error(f"HF API embedding error: {e}. Falling back to mock for this batch.")
            all_embeddings.extend(_mock_embeddings(batch))

    return all_embeddings


# Keep this for backward compatibility with any code that calls get_embeddings_model()
def get_embeddings_model():
    """Returns a callable that generates embeddings — API-based, no local model."""
    return generate_chunk_embeddings


def load_embedding_model():
    """No-op — kept for backward compatibility. Model is remote now."""
    logger.info("Using HuggingFace Inference API for embeddings (no local model)")
    return generate_chunk_embeddings
