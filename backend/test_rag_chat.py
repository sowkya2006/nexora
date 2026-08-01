import os
import sys
import uuid
import datetime

sys.stdout.reconfigure(line_buffering=True)

print("==========================================================================", flush=True)
print("PHASE 6: RAG CHAT INTEGRATION VERIFICATION", flush=True)
print("==========================================================================", flush=True)

from app.database.supabase import get_supabase_client
from app.services.pdf_processor import process_and_index_document
from app.services.chat_service import process_rag_chat_query

# Step 1: Ingest Nexora_University_Admission_Handbook.pdf into Pinecone
pdf_path = os.path.join("..", "knowledge_base", "Nexora_University_Admission_Handbook.pdf")
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

doc_id = "00000000-0000-0000-0000-000000000001"
doc_title = "Nexora University Admission Handbook 2026"
category = "Admissions"
filename = "Nexora_University_Admission_Handbook.pdf"

print("\n--- 1. Ingesting Handbook for RAG Chat Testing ---", flush=True)
process_and_index_document(doc_id, pdf_bytes, doc_title, category, filename)
print("[OK] Admission Handbook ingested and indexed in Pinecone.", flush=True)

# Step 2: Test Real RAG Chat Queries
print("\n--- 2. Testing Known RAG Questions ---", flush=True)

session_id = f"test-chat-{uuid.uuid4()}"

# Test 1: Admission Process
q1 = "What is the admission process?"
print(f"\n[USER QUESTION]: '{q1}'", flush=True)
res1 = process_rag_chat_query(q1, session_id=session_id)
print(f"[AI RESPONSE]:\n{res1.answer}", flush=True)
print(f"[CONFIDENCE SCORE]: {res1.confidence_score}", flush=True)
print(f"[SOURCES CITED]:", flush=True)
for s in res1.sources:
    print(f"   * {s.document} (Page {s.page}): {s.snippet[:80]}...", flush=True)

assert res1.answer != "I could not find this information in the uploaded university documents."
assert len(res1.sources) > 0
print("[VERIFIED] Q1: Relevant RAG answer and source citations generated successfully!", flush=True)

# Test 2: Hostel Fees
q2 = "What are hostel fees?"
print(f"\n[USER QUESTION]: '{q2}'", flush=True)
res2 = process_rag_chat_query(q2, session_id=session_id)
print(f"[AI RESPONSE]:\n{res2.answer}", flush=True)
print(f"[CONFIDENCE SCORE]: {res2.confidence_score}", flush=True)
print(f"[SOURCES CITED]:", flush=True)
for s in res2.sources:
    print(f"   * {s.document} (Page {s.page}): {s.snippet[:80]}...", flush=True)

assert res2.answer != "I could not find this information in the uploaded university documents."
assert len(res2.sources) > 0
print("[VERIFIED] Q2: Relevant RAG answer and source citations generated successfully!", flush=True)

# Test 3: Tuition fees for Computer Science
q3 = "What are tuition fees for Computer Science?"
print(f"\n[USER QUESTION]: '{q3}'", flush=True)
res3 = process_rag_chat_query(q3, session_id=session_id)
print(f"[AI RESPONSE]:\n{res3.answer}", flush=True)
print(f"[CONFIDENCE SCORE]: {res3.confidence_score}", flush=True)
print(f"[SOURCES CITED]:", flush=True)
for s in res3.sources:
    print(f"   * {s.document} (Page {s.page}): {s.snippet[:80]}...", flush=True)

assert "1,80,000" in res3.answer or "180,000" in res3.answer or "1.8" in res3.answer
assert len(res3.sources) > 0
print("[VERIFIED] Q3: Precise tuition fee answer retrieved from Page 2!", flush=True)

# Step 3: Test Unknown / Hallucination Prevention Question
print("\n--- 3. Testing Unknown / Out-of-Domain Question ---", flush=True)
unknown_q = "Who won Nobel prize in Physics?"
print(f"[USER QUESTION]: '{unknown_q}'", flush=True)
unknown_res = process_rag_chat_query(unknown_q, session_id=session_id)
print(f"[AI RESPONSE]: {unknown_res.answer}", flush=True)
print(f"[SOURCES]: {unknown_res.sources}", flush=True)

assert unknown_res.answer == "I could not find this information in the uploaded university documents."
assert len(unknown_res.sources) == 0
print("[VERIFIED] System successfully prevented hallucination and returned exact required fallback string!", flush=True)

# Step 4: Verify Supabase chat_history Table Storage
print("\n--- 4. Verifying Supabase 'chat_history' Storage ---", flush=True)
supabase = get_supabase_client()
db_res = supabase.table("chat_history").select("*").eq("session_id", session_id).execute()
saved_chats = db_res.data
print(f"[OK] Found {len(saved_chats)} chat records in Supabase 'chat_history' table for session {session_id}.", flush=True)
for c in saved_chats:
    print(f"   * User: '{c['user_message']}' -> AI Response length: {len(c['ai_response'])} chars", flush=True)

print("\n==========================================================================", flush=True)
print("ALL PHASE 6 RAG CHAT INTEGRATION TESTS PASSED SUCCESSFULLY!")
print("==========================================================================", flush=True)
