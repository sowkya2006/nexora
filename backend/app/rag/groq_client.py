from functools import lru_cache

from langchain_groq import ChatGroq

from app.config import settings


@lru_cache
def get_groq_client() -> ChatGroq:
    """
    Returns a cached Groq LLM client (Llama 3.3 70B Instruct).
    Used by the RAG pipeline to generate final chatbot responses.
    """
    return ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=0.1,
    )
