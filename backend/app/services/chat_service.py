import re
import json
import uuid
import datetime
import logging
from typing import Dict, Any, List, Optional, Tuple

from app.rag.embeddings import generate_chunk_embeddings
from app.rag.pinecone_client import get_pinecone_index
from app.rag.groq_client import get_groq_client
from app.database.supabase import get_supabase_client
from app.schemas.api import SourceReference, ChatQueryResponse

logger = logging.getLogger(__name__)

FALLBACK_NO_INFO_MESSAGE = "I could not find this information in the uploaded university documents."

# ---------------------------------------------------------------------------
# 1. Intent Detection Map & Document Priority Mapping
# ---------------------------------------------------------------------------
INTENT_DOCUMENT_MAP = {
    "admission": ["Admission Brochure 2026", "Admission Brochure", "Course Catalog and Programs 2026"],
    "fees": ["Fee Structure 2026", "Fee Structure", "Hostel Rules and Fees 2026"],
    "hostel": ["Hostel Rules and Fees 2026", "Hostel Handbook", "Campus Facilities Guide 2026"],
    "placements": ["Placement Brochure 2026", "Placement Brochure"],
    "scholarships": ["Scholarship Handbook 2026", "Scholarship Handbook"],
    "library": ["Library Guide 2026", "Library Guide"],
    "departments": ["Department Handbook 2026", "Course Catalog and Programs 2026"],
    "faculty": ["Department Handbook 2026", "Academic Calendar 2026"],
    "events": ["Academic Calendar 2026"],
    "documents": ["Student Code of Conduct 2026", "Examination Regulations 2026"],
    "downloads": ["Admission Brochure 2026", "Fee Structure 2026", "Hostel Rules and Fees 2026"],
    "navigation": ["Campus Facilities Guide 2026", "Transport Handbook 2026"],
}

PDF_DIRECT_MAPPING = {
    "hostel": ("Hostel Rules and Fees 2026", "Hostel_Rules_and_Fees_2026.pdf"),
    "fee": ("Fee Structure 2026", "Fee_Structure_2026.pdf"),
    "admission": ("Admission Brochure 2026", "Admission_Brochure_2026.pdf"),
    "calendar": ("Academic Calendar 2026", "Academic_Calendar_2026.pdf"),
    "course": ("Course Catalog and Programs 2026", "Course_Catalog_and_Programs.pdf"),
    "placement": ("Placement Brochure 2026", "Placement_Brochure_2026.pdf"),
    "scholarship": ("Scholarship Handbook 2026", "Scholarship_Handbook_2026.pdf"),
    "library": ("Library Guide 2026", "Library_Guide_2026.pdf"),
    "transport": ("Transport Handbook 2026", "Transport_Handbook_2026.pdf"),
    "conduct": ("Student Code of Conduct 2026", "Student_Code_of_Conduct_2026.pdf"),
    "facility": ("Campus Facilities Guide 2026", "Campus_Facilities_Guide_2026.pdf"),
    "exam": ("Examination Regulations 2026", "Examination_Regulations_2026.pdf"),
    "department": ("Department Handbook 2026", "Department_Handbook_2026.pdf"),
}


def _detect_intent(message: str) -> str:
    """Classify user query intent using fast pattern matching and rules."""
    msg = message.lower().strip()

    # Greetings & Small Talk
    if re.search(r"^\b(hi|hello|hey|greetings|good morning|good afternoon|good evening|howdy)\b", msg) or msg in ["who are you", "what is your name", "how are you"]:
        return "greeting"

    if any(k in msg for k in ["thanks", "thank you", "cool", "great", "nice", "awesome"]):
        return "smalltalk"

    if any(k in msg for k in ["download", "get pdf", "show pdf", "view pdf"]):
        return "downloads"
    if any(k in msg for k in ["admission", "apply", "application", "eligibility", "entrance", "intake"]):
        return "admission"
    if any(k in msg for k in ["hostel", "room", "mess", "dorm", "accommodation"]):
        return "hostel"
    if any(k in msg for k in ["fee", "tuition", "cost", "payment", "installment"]):
        return "fees"
    if any(k in msg for k in ["placement", "job", "package", "recruiter", "salary", "internship"]):
        return "placements"
    if any(k in msg for k in ["scholarship", "financial aid", "stipend", "waiver"]):
        return "scholarships"
    if any(k in msg for k in ["library", "books", "journal", "reading room"]):
        return "library"
    if any(k in msg for k in ["faculty", "professor", "teacher", "dean", "hod"]):
        return "faculty"
    if any(k in msg for k in ["department", "branch", "computer science", "engineering", "btech"]):
        return "departments"

    if any(k in msg for k in ["event", "fest", "calendar", "holiday", "schedule", "exam"]):
        return "events"
    if any(k in msg for k in ["bus", "transport", "route", "campus", "map", "location"]):
        return "navigation"
    if any(k in msg for k in ["code of conduct", "rule", "policy", "regulation"]):
        return "documents"

    return "unknown"


def _rewrite_query_with_context(question: str, history: List[dict]) -> str:
    """
    Rewrite short/follow-up questions using prior conversation context.
    Example: 'How can I apply for admission?' -> 'Explain complete process'
    Rewritten: 'Explain complete admission process at Nexora University.'
    """
    if not history:
        return question

    q_lower = question.lower().strip()

    is_short_followup = (
        len(q_lower.split()) <= 6 or
        any(phrase in q_lower for phrase in [
            "explain process", "explain complete process", "how does it work",
            "tell me in detail", "what is the procedure", "explain in detail",
            "what are the steps", "give details", "explain eligibility", "what about fees"
        ])
    )

    if not is_short_followup:
        return question

    last_user_msg = ""
    for msg in reversed(history):
        role = msg.get("role", "")
        content = msg.get("content", "")
        if role == "user" and content:
            last_user_msg = content
            break

    if not last_user_msg:
        return question

    last_intent = _detect_intent(last_user_msg)
    if last_intent not in ["unknown", "greeting", "smalltalk"]:
        rewritten = f"{question} for {last_intent} process at Nexora University"
        logger.info(f"Query Rewritten: '{question}' -> '{rewritten}'")
        return rewritten

    return question



def _retrieve_and_rerank_chunks(
    query_vector: List[float],
    intent: str,
    top_k: int = 10
) -> List[dict]:
    """
    Retrieve chunks from Pinecone, expand neighboring context, and perform smart reranking.
    """
    pinecone_index = get_pinecone_index()
    
    # Primary Pinecone vector query
    query_res = pinecone_index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )
    
    matches = query_res.matches if hasattr(query_res, "matches") else []
    if not matches:
        return []

    priority_docs = INTENT_DOCUMENT_MAP.get(intent, [])
    
    extracted_chunks = []
    seen_ids = set()

    for match in matches:
        meta = match.metadata or {}
        doc_id = meta.get("document_id", "")
        doc_title = meta.get("title", meta.get("document_name", "University Document"))
        page_num = int(meta.get("page_number", meta.get("page", 1)))
        chunk_num = int(meta.get("chunk_number", 1))
        text = meta.get("text", "").strip()
        score = float(getattr(match, "score", 0.0))

        if not text:
            continue

        # Document Priority Score Booster (+0.15 for matching primary documents)
        is_priority_doc = any(p_doc.lower() in doc_title.lower() for p_doc in priority_docs)
        adjusted_score = score + (0.15 if is_priority_doc else 0.0)

        chunk_key = (doc_title, page_num, chunk_num)
        if chunk_key not in seen_ids:
            seen_ids.add(chunk_key)
            extracted_chunks.append({
                "document_id": doc_id,
                "title": doc_title,
                "page": page_num,
                "chunk_number": chunk_num,
                "text": text,
                "raw_score": score,
                "score": adjusted_score,
                "is_priority": is_priority_doc,
            })

    # Sort chunks by boosted score descending
    extracted_chunks.sort(key=lambda c: c["score"], reverse=True)
    
    # Filter out low similarity chunks — lowered to 0.1 to handle cross-model embedding differences
    filtered_chunks = [c for c in extracted_chunks if c["raw_score"] >= 0.1]
    if not filtered_chunks:
        return []

    # ---------------------------------------------------------------------------
    # Context Window Expansion: Fetch neighboring chunks (previous/next)
    # ---------------------------------------------------------------------------
    top_chunks = filtered_chunks[:4]
    expanded_context_chunks = []
    seen_context_keys = set()

    for chunk in top_chunks:
        c_key = (chunk["title"], chunk["page"], chunk["chunk_number"])
        if c_key not in seen_context_keys:
            seen_context_keys.add(c_key)
            expanded_context_chunks.append(chunk)

        # Attempt neighbor lookup in remaining matches
        neighbor_nums = [chunk["chunk_number"] - 1, chunk["chunk_number"] + 1]
        for match in matches:
            meta = match.metadata or {}
            m_title = meta.get("title", meta.get("document_name", ""))
            m_chunk_num = int(meta.get("chunk_number", -99))
            m_page = int(meta.get("page_number", meta.get("page", 1)))
            
            if m_title == chunk["title"] and m_chunk_num in neighbor_nums:
                n_key = (m_title, m_page, m_chunk_num)
                if n_key not in seen_context_keys:
                    seen_context_keys.add(n_key)
                    expanded_context_chunks.append({
                        "document_id": meta.get("document_id", ""),
                        "title": m_title,
                        "page": m_page,
                        "chunk_number": m_chunk_num,
                        "text": meta.get("text", "").strip(),
                        "raw_score": float(getattr(match, "score", 0.0)),
                        "score": float(getattr(match, "score", 0.0)),
                        "is_priority": chunk["is_priority"],
                    })

    # Sort final expanded context by document and page number for smooth natural ordering
    expanded_context_chunks.sort(key=lambda c: (c["title"], c["page"], c["chunk_number"]))
    return expanded_context_chunks


def process_rag_chat_query(
    question: str,
    session_id: Optional[str] = None,
    history: List[dict] = []
) -> ChatQueryResponse:
    """
    Phase 13 Enhanced Conversational RAG Pipeline:
    1. Intent Classification
    2. Conversational Memory & Contextual Query Rewriting
    3. Document-Prioritized & Window-Expanded Retrieval
    4. Senior University Counselor Synthesis (SOP, Bullet points, Notes, Warnings)
    5. Bottom Citation Assembly & Strict Hallucination Fallback
    """
    if not session_id:
        session_id = str(uuid.uuid4())

    # Step 1: Intent Detection
    intent = _detect_intent(question)

    # Handle Greetings & Small Talk directly
    if intent == "greeting":
        answer = (
            "Hello! I am **UniSphere AI**, the official conversational assistant for Nexora University.\n\n"
            "I can assist you with comprehensive information regarding:\n"
            "- **Admissions & Eligibility Criteria**\n"
            "- **Tuition & Hostel Fee Structure**\n"
            "- **Scholarships & Financial Aid**\n"
            "- **Placement Records & Recruiters**\n"
            "- **Campus Facilities & Academic Guidelines**\n\n"
            "How may I assist you today?"
        )
        _save_chat_history(session_id, question, answer, [])
        return ChatQueryResponse(
            answer=answer,
            sources=[],
            confidence_score=1.0
        )

    if intent == "smalltalk":
        answer = "You're very welcome! Feel free to ask if you need any more information regarding admissions, fees, hostel, or campus life at Nexora University."
        _save_chat_history(session_id, question, answer, [])
        return ChatQueryResponse(
            answer=answer,
            sources=[],
            confidence_score=1.0
        )


    # Handle Direct PDF Download Request
    if intent == "downloads":
        q_low = question.lower()
        for key, (doc_title, file_name) in PDF_DIRECT_MAPPING.items():
            if key in q_low:
                answer = (
                    f"Here is the official **{doc_title}** document for Nexora University. "
                    "You can view or download the complete PDF using the verified reference link below."
                )
                sources = [
                    SourceReference(
                        document=doc_title,
                        page=1,
                        snippet=f"Official PDF document: {file_name}"
                    )
                ]
                _save_chat_history(session_id, question, answer, sources)
                return ChatQueryResponse(
                    answer=answer,
                    sources=sources,
                    confidence_score=1.0
                )

    # Step 2: Multi-turn Contextual Query Rewriting
    search_query = _rewrite_query_with_context(question, history)

    # Step 3: Embed Query & Retrieve Prioritized/Expanded Chunks
    query_vector = generate_chunk_embeddings([search_query])[0]
    chunks = _retrieve_and_rerank_chunks(query_vector, intent, top_k=10)

    # Strict Fallback if no relevant chunks found
    if not chunks:
        answer = FALLBACK_NO_INFO_MESSAGE
        sources = []
        _save_chat_history(session_id, question, answer, sources)
        return ChatQueryResponse(
            answer=answer,
            sources=sources,
            confidence_score=0.0
        )

    top_raw_score = max(c["raw_score"] for c in chunks)
    confidence_score = round(min(max(top_raw_score, 0.0), 1.0), 2)

    # Step 4: Build Context String & Verified Citations
    context_blocks = []
    sources: List[SourceReference] = []
    seen_sources = set()

    for c in chunks:
        doc_title = c["title"]
        page_num = c["page"]
        context_blocks.append(f"[Document: {doc_title} | Page {page_num}]\n{c['text']}")

        src_key = (doc_title, page_num)
        if src_key not in seen_sources:
            seen_sources.add(src_key)
            snippet = c["text"][:160] + ("..." if len(c["text"]) > 160 else "")
            sources.append(
                SourceReference(
                    document=doc_title,
                    page=page_num,
                    snippet=snippet
                )
            )

    sources = sources[:3] # Top 3 distinct verified sources
    context_str = "\n\n---\n\n".join(context_blocks)

    # Step 5: Counselor Synthesis Prompting (SOP Style, Zero Hallucination)
    system_prompt = (
        "You are UniSphere AI, the senior official university counselor for Nexora University.\n"
        "Your task is to provide clear, professional, well-structured, and highly informative answers based ONLY on the official document context provided.\n\n"
        "STRICT GUIDELINES:\n"
        "1. NEVER dump raw document text. Always organize, summarize, and explain naturally like a helpful counselor.\n"
        "2. If the user asks for a process, procedure, or how something works, provide a clear, step-by-step SOP style response with clear section headings.\n"
        "3. Use structured formatting:\n"
        "   - Clear Markdown Headings (e.g. ### Overview, ### Step-by-Step Procedure)\n"
        "   - Bullet points & numbered lists\n"
        "   - **Important Notes** or **Tips / Warnings** where relevant\n"
        "4. If information comes from multiple documents, merge it into one seamless, coherent answer without saying 'Document A says' or 'Document B says'.\n"
        "5. Do NOT include source citations or page numbers inside the answer body; sources will be displayed automatically at the bottom.\n"
        "6. ABSOLUTE ZERO HALLUCINATION RULE: If the answer cannot be determined from the provided context, output EXACTLY:\n"
        "'I could not find this information in the uploaded university documents.'\n"
    )

    user_message = (
        f"Context from University Documents:\n{context_str}\n\n"
        f"User Question: {question}\n"
        f"Rewritten Query Context: {search_query}\n\n"
        "Please construct a counselor-style response adhering strictly to all rules:"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    try:
        groq_llm = get_groq_client()
        llm_response = groq_llm.invoke(messages)
        answer = str(llm_response.content).strip()

        # Enforce exact fallback string if LLM indicates missing context
        if (
            "could not find this information" in answer.lower() or
            "not available in the context" in answer.lower() or
            "cannot find" in answer.lower()
        ):
            answer = FALLBACK_NO_INFO_MESSAGE
            sources = []

    except Exception as err:
        logger.error(f"Groq LLM invocation error: {err}")
        # Structured fallback if Groq API fails
        answer = (
            f"### Official Information Summary\n\n"
            f"Based on official Nexora University records:\n\n"
            f"{chunks[0]['text']}"
        )

    # Step 6: Save Chat History
    _save_chat_history(session_id, question, answer, sources)

    return ChatQueryResponse(
        answer=answer,
        sources=sources,
        confidence_score=confidence_score
    )


def _save_chat_history(session_id: str, question: str, answer: str, sources: List[SourceReference]):
    """Store chat interaction in Supabase chat_history table."""
    try:
        supabase = get_supabase_client()
        serialized_sources = json.dumps([s.model_dump() for s in sources])
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

        record = {
            "session_id": session_id,
            "user_message": question,
            "ai_response": answer,
            "source_document": serialized_sources,
            "created_at": now_iso
        }
        supabase.table("chat_history").insert(record).execute()
    except Exception as e:
        logger.warning(f"Supabase chat_history storage note: {e}")
