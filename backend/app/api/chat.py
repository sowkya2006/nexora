from fastapi import APIRouter, HTTPException, status
from app.schemas.api import ChatQueryRequest, ChatQueryResponse
from app.services.chat_service import process_rag_chat_query

router = APIRouter()


@router.post("/query", response_model=ChatQueryResponse, status_code=status.HTTP_200_OK)
async def chat_query(body: ChatQueryRequest):
    """
    Process RAG chat query:
    Vector search -> Pinecone retrieval -> Groq LLM -> Response with Sources.
    """
    if not body.question or not body.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question text cannot be empty."
        )

    try:
        return process_rag_chat_query(
            question=body.question.strip(),
            session_id=body.session_id,
            history=body.history
        )
    except Exception as e:
        err_msg = str(e)
        if "401" in err_msg or "Invalid API key" in err_msg or "api_key" in err_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing Groq API Key. Please configure your GROQ_API_KEY in backend/.env file."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat service error: {err_msg}"
        )
