"""
UniSphere AI – RAG Chat Service (Phase 14 – Complete Fix)
=========================================================
Key fixes:
- Accepts BOTH old and new metadata key schemas (document_name / title, page / page_number, etc.)
- top_k = 20 for wide retrieval
- Intent-based document priority boost (+0.30 for primary docs, +0.15 for secondary)
- Groups and merges chunks from the same document before sending to LLM
- Score threshold = 0.005 (works with low HF API cosine scores)
- Prompt instructs LLM to use ALL retrieved chunks and list every item found
- No citations from unrelated documents
"""
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

FALLBACK_NO_INFO_MESSAGE = (
    "I could not find this information in the uploaded university documents. "
    "Please contact the university office directly or check the official website."
)

# ---------------------------------------------------------------------------
# Intent Detection
# ---------------------------------------------------------------------------
INTENT_PATTERNS: Dict[str, List[str]] = {
    "greeting":    [r"^\s*(hi|hello|hey|greetings|good\s+(morning|afternoon|evening)|howdy)\b",
                    r"^(who are you|what is your name|how are you)\s*\??\s*$"],
    "smalltalk":   ["thanks", "thank you", "cool", "great", "nice", "awesome", "bye", "goodbye"],
    "downloads":   ["download", "get pdf", "show pdf", "view pdf", "brochure"],
    "courses":     ["course", "programme", "program", "b.tech", "btech", "m.tech", "mtech",
                    "mba", "mca", "bca", "bba", "bsc", "degree", "curriculum", "syllabus",
                    "what courses", "available courses", "study", "specializ"],
    "admission":   ["admission", "apply", "application", "eligibility", "entrance",
                    "intake", "jee", "eamcet", "nexet", "cutoff", "merit list"],
    "hostel":      ["hostel", "room", "mess", "dorm", "accommodation", "warden", "curfew",
                    "residential", "pg block", "hostel fee"],
    "fees":        ["fee", "tuition", "cost", "payment", "installment", "caution deposit",
                    "refund", "challan"],
    "placements":  ["placement", "job", "package", "lpa", "recruiter", "salary",
                    "internship", "campus drive", "cdc", "career"],
    "scholarships":["scholarship", "financial aid", "stipend", "waiver", "merit award",
                    "gate fellowship", "nri scholarship"],
    "library":     ["library", "books", "journal", "reading room", "digital resource",
                    "borrowing", "inflibnet", "ieee"],
    "faculty":     ["faculty", "professor", "teacher", "dean", "hod", "head of department",
                    "lecturer", "staff", "cabin", "office hours", "email of"],
    "departments": ["department", "branch", "computer science", "cse", "ece", "mechanical",
                    "civil", "eee", "aids", "research centre"],
    "transport":   ["bus", "transport", "route", "commute", "pickup", "drop",
                    "bus pass", "timing"],
    "events":      ["event", "fest", "festival", "cultural", "hackathon", "sports",
                    "academic calendar", "holiday", "schedule", "nexfest"],
    "research":    ["research", "phd", "doctorate", "publication", "patent",
                    "innovation", "incubation", "nexhub", "startup"],
    "clubs":       ["club", "society", "student activity", "nss", "ncc",
                    "cultural club", "technical club"],
    "campus":      ["campus", "facility", "gym", "cafeteria", "sports complex",
                    "medical centre", "atm", "bank"],
    "exams":       ["exam", "examination", "grade", "cgpa", "backlog", "revaluation",
                    "attendance", "internal assessment", "result"],
}

# ---------------------------------------------------------------------------
# Intent → Primary document names (must match exactly what is stored in Pinecone metadata)
# ---------------------------------------------------------------------------
INTENT_DOCUMENT_MAP: Dict[str, List[str]] = {
    "courses":      ["Course Catalog & Programmes",   "Academic Regulations 2026",
                     "Department Handbook: CSE"],
    "admission":    ["Admission Handbook 2026",        "Course Catalog & Programmes"],
    "hostel":       ["Hostel & Accommodation Guide"],
    "fees":         ["Fee Structure 2026-27",          "Hostel & Accommodation Guide"],
    "placements":   ["Placement Report 2026"],
    "scholarships": ["Scholarships & Financial Aid 2026"],
    "library":      ["Library Guide 2026"],
    "faculty":      ["Department Handbook: CSE"],
    "departments":  ["Department Handbook: CSE",       "Course Catalog & Programmes"],
    "transport":    ["Transport Guide 2026"],
    "events":       ["Academic Calendar 2026-27"],
    "research":     ["Research & Innovation Handbook"],
    "clubs":        ["Student Handbook & Code of Conduct", "Campus Facilities Guide"],
    "campus":       ["Campus Facilities Guide"],
    "exams":        ["Academic Regulations 2026",      "Academic Calendar 2026-27"],
}

# Intent → secondary documents (smaller boost)
INTENT_SECONDARY_MAP: Dict[str, List[str]] = {
    "courses":      ["Admission Handbook 2026"],
    "admission":    ["Academic Regulations 2026",  "Scholarships & Financial Aid 2026"],
    "hostel":       ["Fee Structure 2026-27"],
    "fees":         ["Scholarships & Financial Aid 2026"],
    "placements":   ["Campus Facilities Guide"],
    "scholarships": ["Admission Handbook 2026",    "Fee Structure 2026-27"],
    "faculty":      ["Academic Regulations 2026"],
    "departments":  ["Academic Regulations 2026"],
}

# Direct PDF download mapping (filename must exist in knowledge_base)
PDF_DIRECT_MAPPING = {
    "hostel":       ("Hostel & Accommodation Guide",        "Hostel_Accommodation_Guide.pdf"),
    "fee":          ("Fee Structure 2026-27",               "Fee_Structure_2026.pdf"),
    "admission":    ("Admission Handbook 2026",             "Admission_Handbook_2026.pdf"),
    "calendar":     ("Academic Calendar 2026-27",           "Academic_Calendar_2026.pdf"),
    "course":       ("Course Catalog & Programmes",         "Course_Catalog_and_Programs.pdf"),
    "placement":    ("Placement Report 2026",               "Placement_Report_2026.pdf"),
    "scholarship":  ("Scholarships & Financial Aid 2026",   "Scholarships_Financial_Aid_2026.pdf"),
    "library":      ("Library Guide 2026",                  "Library_Guide_2026.pdf"),
    "transport":    ("Transport Guide 2026",                "Transport_Guide_2026.pdf"),
    "conduct":      ("Student Handbook & Code of Conduct",  "Student_Handbook_Code_of_Conduct.pdf"),
    "facility":     ("Campus Facilities Guide",             "Campus_Facilities_Guide.pdf"),
    "research":     ("Research & Innovation Handbook",      "Research_Innovation_Handbook.pdf"),
    "department":   ("Department Handbook: CSE",            "Department_Handbook_CSE.pdf"),
    "regulation":   ("Academic Regulations 2026",           "Academic_Regulations_2026.pdf"),
}


def _detect_intent(message: str) -> str:
    """Classify query intent using keyword patterns. Returns the most specific match."""
    msg = message.lower().strip()

    # Greeting — regex check
    for pattern in INTENT_PATTERNS["greeting"]:
        if re.search(pattern, msg):
            return "greeting"

    # Smalltalk — keyword check
    if any(k in msg for k in INTENT_PATTERNS["smalltalk"]):
        return "smalltalk"

    # Score-based: count keyword matches per intent and pick the highest
    scores: Dict[str, int] = {}
    for intent, keywords in INTENT_PATTERNS.items():
        if intent in ("greeting", "smalltalk"):
            continue
        count = sum(1 for kw in keywords if kw in msg)
        if count > 0:
            scores[intent] = count

    if scores:
        return max(scores, key=lambda k: scores[k])

    return "unknown"


def _get_meta(meta: dict, *keys, default=""):
    """Safely extract a value from metadata trying multiple possible key names."""
    for k in keys:
        v = meta.get(k)
        if v is not None:
            return v
    return default


def _rewrite_query(question: str, history: List[dict]) -> str:
    """
    Expand short follow-up questions using conversation history context.
    """
    if not history:
        return question

    q = question.lower().strip()
    followup_signals = [
        "explain", "tell me more", "what about", "give details", "how does",
        "what is the procedure", "steps", "process", "more info", "elaborate"
    ]
    is_followup = len(q.split()) <= 5 or any(sig in q for sig in followup_signals)
    if not is_followup:
        return question

    # Find last meaningful user message
    for msg in reversed(history):
        if msg.get("role") == "user" and msg.get("content", "").strip():
            prev = msg["content"].strip()
            if prev.lower() != question.lower():
                rewritten = f"{question} regarding {prev} at Nexora University"
                logger.info(f"Query rewritten: '{question}' -> '{rewritten}'")
                return rewritten
            break

    return question


def _retrieve_and_group_chunks(
    query_vector: List[float],
    intent: str,
    top_k: int = 20,
) -> List[dict]:
    """
    Retrieves top_k chunks from Pinecone, applies priority boosts,
    groups by document, merges adjacent chunks, and returns
    a ranked list ready for the LLM context.
    """
    pinecone_index = get_pinecone_index()

    query_res = pinecone_index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )
    matches = query_res.matches if hasattr(query_res, "matches") else []
    if not matches:
        logger.info("Pinecone returned 0 matches")
        return []

    primary_docs   = [d.lower() for d in INTENT_DOCUMENT_MAP.get(intent, [])]
    secondary_docs = [d.lower() for d in INTENT_SECONDARY_MAP.get(intent, [])]

    # ── Parse every match ─────────────────────────────────────────────────
    raw_chunks: List[dict] = []
    for match in matches:
        meta = match.metadata or {}
        score = float(getattr(match, "score", 0.0))

        # Accept both old metadata schema (document_name / page / chunk_index)
        # and new schema (title / page_number / chunk_number)
        doc_name  = str(_get_meta(meta, "document_name", "title",        default="University Document"))
        page_num  = int(_get_meta(meta, "page_number",   "page",         default=1))
        chunk_num = int(_get_meta(meta, "chunk_number",  "chunk_index",  default=0))
        doc_id    = str(_get_meta(meta, "document_id",                   default=""))
        text      = str(_get_meta(meta, "text",                          default="")).strip()
        category  = str(_get_meta(meta, "category",                      default=""))
        file_name = str(_get_meta(meta, "file_name",                     default=""))
        file_url  = str(_get_meta(meta, "file_url",                      default=""))

        if not text:
            continue

        # Priority boost
        doc_lower = doc_name.lower()
        if any(p in doc_lower for p in primary_docs):
            boosted = score + 0.30
            priority = "primary"
        elif any(s in doc_lower for s in secondary_docs):
            boosted = score + 0.15
            priority = "secondary"
        else:
            boosted = score
            priority = "none"

        raw_chunks.append({
            "doc_name":  doc_name,
            "doc_id":    doc_id,
            "page":      page_num,
            "chunk_num": chunk_num,
            "text":      text,
            "raw_score": score,
            "score":     boosted,
            "priority":  priority,
            "category":  category,
            "file_name": file_name,
            "file_url":  file_url,
        })

    # ── Log retrieval debug info ───────────────────────────────────────────
    logger.info(f"[RAG] Intent: {intent} | Retrieved: {len(raw_chunks)} chunks from Pinecone")
    for c in raw_chunks[:5]:
        logger.info(f"  score={c['raw_score']:.4f} boosted={c['score']:.4f} "
                    f"priority={c['priority']} doc={c['doc_name']} p={c['page']}")

    # ── Apply minimum score filter ─────────────────────────────────────────
    # Threshold 0.005 — intentionally very low because HF API cosine scores
    # for these short-text PDF chunks are uniformly small (0.01 – 0.10)
    MIN_SCORE = 0.005
    filtered = [c for c in raw_chunks if c["raw_score"] >= MIN_SCORE]
    if not filtered:
        logger.warning("[RAG] All chunks below threshold — returning all raw matches")
        filtered = sorted(raw_chunks, key=lambda c: c["score"], reverse=True)

    # ── Sort by boosted score ──────────────────────────────────────────────
    filtered.sort(key=lambda c: c["score"], reverse=True)

    # ── Group chunks by document, merge adjacent ───────────────────────────
    # Key: doc_name → list of chunks sorted by page, chunk_num
    from collections import defaultdict
    doc_groups: Dict[str, List[dict]] = defaultdict(list)
    for c in filtered:
        doc_groups[c["doc_name"]].append(c)

    for doc in doc_groups:
        doc_groups[doc].sort(key=lambda c: (c["page"], c["chunk_num"]))

    # ── Build merged context blocks per document ───────────────────────────
    merged_blocks: List[dict] = []
    for doc_name, chunks in doc_groups.items():
        # Merge adjacent chunks (same page or sequential chunk numbers)
        merged_texts: List[str] = []
        merged_pages: List[int] = []
        prev_chunk_num = -99

        for c in chunks:
            if c["chunk_num"] == prev_chunk_num + 1 and merged_texts:
                # Adjacent — append without repeating
                merged_texts[-1] = merged_texts[-1] + " " + c["text"]
                if c["page"] not in merged_pages:
                    merged_pages.append(c["page"])
            else:
                merged_texts.append(c["text"])
                merged_pages.append(c["page"])
            prev_chunk_num = c["chunk_num"]

        best_score = max(c["score"] for c in chunks)
        best_raw   = max(c["raw_score"] for c in chunks)
        priority   = chunks[0]["priority"]

        merged_blocks.append({
            "doc_name":   doc_name,
            "doc_id":     chunks[0]["doc_id"],
            "pages":      merged_pages,
            "text":       "\n\n".join(merged_texts),
            "score":      best_score,
            "raw_score":  best_raw,
            "priority":   priority,
            "category":   chunks[0]["category"],
            "file_name":  chunks[0]["file_name"],
            "file_url":   chunks[0]["file_url"],
            "chunk_count": len(chunks),
        })

    # ── Sort blocks: primary first, then by score ──────────────────────────
    priority_order = {"primary": 0, "secondary": 1, "none": 2}
    merged_blocks.sort(key=lambda b: (priority_order.get(b["priority"], 2), -b["score"]))

    # ── Filter out unrelated blocks when strong primary results exist ──────
    if primary_docs and any(b["priority"] == "primary" for b in merged_blocks):
        primary_best = max(b["score"] for b in merged_blocks if b["priority"] == "primary")
        # Keep a block only if its score is within 0.20 of primary best, or if it is primary/secondary
        merged_blocks = [
            b for b in merged_blocks
            if b["priority"] in ("primary", "secondary")
            or b["score"] >= primary_best - 0.20
        ]

    logger.info(f"[RAG] Final blocks after grouping: {len(merged_blocks)} documents")
    for b in merged_blocks:
        logger.info(f"  {b['doc_name']} | pages={b['pages']} | "
                    f"chunks={b['chunk_count']} | score={b['score']:.4f} | priority={b['priority']}")

    return merged_blocks


def _build_context_and_sources(
    blocks: List[dict],
    max_context_chars: int = 12000,
) -> Tuple[str, List[SourceReference]]:
    """
    Builds the context string passed to Groq and assembles verified citations.
    Respects a character budget to stay within Groq context limits.
    """
    context_parts: List[str] = []
    sources: List[SourceReference] = []
    seen_docs: set = set()
    total_chars = 0

    for block in blocks:
        doc_name  = block["doc_name"]
        pages_str = ", ".join(str(p) for p in block["pages"])
        text      = block["text"]

        header = f"[Source: {doc_name} | Pages: {pages_str}]"
        block_str = f"{header}\n{text}"

        if total_chars + len(block_str) > max_context_chars:
            # Include a truncated version if budget allows at least 500 chars
            remaining = max_context_chars - total_chars
            if remaining >= 500:
                context_parts.append(f"{header}\n{text[:remaining]}")
                total_chars += remaining
            break

        context_parts.append(block_str)
        total_chars += len(block_str)

        # Add to verified citations (max 5 distinct documents)
        if doc_name not in seen_docs and len(seen_docs) < 5:
            seen_docs.add(doc_name)
            snippet = text[:200].replace("\n", " ").strip()
            sources.append(SourceReference(
                document=doc_name,
                page=block["pages"][0] if block["pages"] else 1,
                snippet=snippet + ("..." if len(text) > 200 else "")
            ))

    context_str = "\n\n═══\n\n".join(context_parts)
    return context_str, sources


SYSTEM_PROMPT = """You are UniSphere AI, the official academic counselor for Nexora University.
You answer student questions using ONLY the official university documents provided in the context.

STRICT RULES:
1. READ every context block carefully before answering.
2. If the question asks for a LIST (courses, facilities, faculty, routes, etc.):
   - List EVERY item found across ALL context blocks — never stop after the first item.
   - Use clear bullet points or numbered lists.
   - If an item has attributes (duration, eligibility, fees), include them.
3. Organise your answer with Markdown headings (###), bullet points, and tables where appropriate.
4. NEVER cite document names or page numbers in the answer body — citations appear separately.
5. NEVER invent information not present in the context.
6. If context is insufficient, respond EXACTLY:
   "I could not find this information in the uploaded university documents."
7. Be comprehensive — a student should get a COMPLETE answer, not a summary.
"""


def process_rag_chat_query(
    question: str,
    session_id: Optional[str] = None,
    history: List[dict] = []
) -> ChatQueryResponse:
    """
    Phase 14 RAG Pipeline:
    1. Intent detection
    2. Greeting / smalltalk fast-path
    3. Download intent fast-path
    4. Query rewriting for follow-ups
    5. Embedding + Pinecone retrieval (top_k=20)
    6. Priority boost + grouping + adjacent-chunk merging
    7. Citation filtering (no unrelated docs)
    8. Groq synthesis with comprehensive prompt
    """
    if not session_id:
        session_id = str(uuid.uuid4())

    intent = _detect_intent(question)
    logger.info(f"[RAG] Question: '{question[:80]}' | Intent: {intent}")

    # ── Greeting ───────────────────────────────────────────────────────────
    if intent == "greeting":
        answer = (
            "Hello! I am **UniSphere AI**, the official assistant for Nexora University.\n\n"
            "I can answer questions about:\n"
            "- **Courses & Curriculum** (B.Tech, M.Tech, MBA, MCA, BCA)\n"
            "- **Admissions & Eligibility**\n"
            "- **Fees & Scholarships**\n"
            "- **Hostel & Campus Life**\n"
            "- **Placements & Recruiters**\n"
            "- **Faculty & Departments**\n"
            "- **Library, Transport & Events**\n\n"
            "How may I assist you today?"
        )
        _save_chat_history(session_id, question, answer, [])
        return ChatQueryResponse(answer=answer, sources=[], confidence_score=1.0)

    # ── Small talk ─────────────────────────────────────────────────────────
    if intent == "smalltalk":
        answer = "You're welcome! Feel free to ask anything about Nexora University."
        _save_chat_history(session_id, question, answer, [])
        return ChatQueryResponse(answer=answer, sources=[], confidence_score=1.0)

    # ── Direct download request ────────────────────────────────────────────
    if intent == "downloads":
        q_low = question.lower()
        for key, (doc_title, file_name) in PDF_DIRECT_MAPPING.items():
            if key in q_low:
                answer = (
                    f"Here is the official **{doc_title}** for Nexora University. "
                    "Click **View PDF** or **Download PDF** on the citation card below."
                )
                sources = [SourceReference(document=doc_title, page=1,
                                            snippet=f"Official PDF: {file_name}")]
                _save_chat_history(session_id, question, answer, sources)
                return ChatQueryResponse(answer=answer, sources=sources, confidence_score=1.0)

    # ── Query rewriting ────────────────────────────────────────────────────
    search_query = _rewrite_query(question, history)

    # ── Embedding ─────────────────────────────────────────────────────────
    query_vector = generate_chunk_embeddings([search_query])[0]

    # ── Retrieval + grouping ───────────────────────────────────────────────
    blocks = _retrieve_and_group_chunks(query_vector, intent, top_k=20)

    if not blocks:
        _save_chat_history(session_id, question, FALLBACK_NO_INFO_MESSAGE, [])
        return ChatQueryResponse(answer=FALLBACK_NO_INFO_MESSAGE, sources=[], confidence_score=0.0)

    # ── Context + citations ────────────────────────────────────────────────
    context_str, sources = _build_context_and_sources(blocks)

    top_score = max(b["raw_score"] for b in blocks)
    confidence = round(min(max(top_score * 5, 0.1), 1.0), 2)  # scale up for display

    # ── LLM synthesis ─────────────────────────────────────────────────────
    user_message = (
        f"Context from Nexora University official documents:\n\n{context_str}\n\n"
        f"Student Question: {question}\n\n"
        "Please provide a complete, well-structured answer using ALL relevant information "
        "from the context above. If the question asks for a list, include every item found."
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": user_message},
    ]

    try:
        groq_llm = get_groq_client()
        response  = groq_llm.invoke(messages)
        answer    = str(response.content).strip()

        # Enforce fallback if LLM says it doesn't know
        no_info_signals = [
            "could not find this information",
            "not available in the context",
            "cannot find",
            "no information provided",
            "documents do not contain",
        ]
        if any(sig in answer.lower() for sig in no_info_signals):
            answer = FALLBACK_NO_INFO_MESSAGE
            sources = []

    except Exception as err:
        logger.error(f"[RAG] Groq error: {err}")
        # Structured fallback: use best block text directly
        best = blocks[0]
        answer = (
            f"### {best['doc_name']}\n\n"
            + best["text"][:1500]
        )

    _save_chat_history(session_id, question, answer, sources)
    return ChatQueryResponse(answer=answer, sources=sources, confidence_score=confidence)


def _save_chat_history(session_id: str, question: str, answer: str,
                       sources: List[SourceReference]) -> None:
    """Persist chat interaction to Supabase chat_history table."""
    try:
        supabase = get_supabase_client()
        supabase.table("chat_history").insert({
            "session_id":      session_id,
            "user_message":    question,
            "ai_response":     answer,
            "source_document": json.dumps([s.model_dump() for s in sources]),
            "created_at":      datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }).execute()
    except Exception as e:
        logger.warning(f"[RAG] chat_history save note: {e}")
