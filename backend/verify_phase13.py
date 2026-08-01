import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai.rag.chain import generate_response, _detect_intent, _rewrite_query

async def run_phase13_tests():
    print("================================================================")
    print("PHASE 13: INTELLIGENT CONVERSATIONAL RAG VERIFICATION SUITE")
    print("================================================ failure/success\n")

    results = []

    # 1. Intent Detection Test
    intents_to_test = [
        ("Hello there!", "greeting"),
        ("Thank you so much!", "smalltalk"),
        ("How can I apply for admission?", "admission"),
        ("What are the hostel room fees?", "hostel"),
        ("What is the tuition fee structure?", "fees"),
        ("Show me placement records", "placements"),
        ("Are there scholarships for students?", "scholarships"),
        ("What are the library timings?", "library"),
        ("Tell me about Computer Science department", "departments"),
        ("Who is the Dean of engineering?", "faculty"),
        ("When are the end semester exams?", "events"),
        ("Where is the campus bus route?", "navigation"),
        ("Download Admission Brochure PDF", "downloads"),
    ]

    print("--- 1. INTENT DETECTION TESTS ---")
    intent_passed = True
    for text, expected in intents_to_test:
        detected = _detect_intent(text)
        ok = detected == expected
        if not ok:
            intent_passed = False
        print(f"[{'PASS' if ok else 'FAIL'}] '{text}' -> Detected: {detected} | Expected: {expected}")
    results.append(("Intent Detection Coverage", intent_passed))

    # 2. Conversational Memory & Query Rewriting Test
    print("\n--- 2. CONVERSATIONAL MEMORY & QUERY REWRITING TESTS ---")
    history = [{"role": "user", "content": "How can I apply for admission?"}]
    followup = "Explain complete process"
    rewritten = _rewrite_query(followup, history)
    print(f"Original follow-up: '{followup}'")
    print(f"Rewritten Query   : '{rewritten}'")
    rewrite_ok = "admission" in rewritten.lower()
    print(f"[{'PASS' if rewrite_ok else 'FAIL'}] Multi-turn query correctly resolved topic context.")
    results.append(("Query Rewriting & Context Memory", rewrite_ok))

    # 3. Multi-turn Conversation Pipeline Test
    print("\n--- 3. MULTI-TURN RAG CONVERSATION TEST ---")
    res1 = await generate_response("How can I apply for admission?", [])
    print(f"Turn 1 Intent: {res1.get('intent')}")
    print(f"Turn 1 Answer snippet: {res1.get('answer')[:120]}...\n")

    history.append({"role": "assistant", "content": res1.get("answer")})
    res2 = await generate_response("Explain complete process", history)
    print(f"Turn 2 Intent: {res2.get('intent')}")
    print(f"Turn 2 Answer snippet: {res2.get('answer')[:150]}...\n")
    turn2_ok = len(res2.get("answer")) > 50 and "I could not find" not in res2.get("answer")
    results.append(("Multi-Turn Conversation Flow", turn2_ok))

    # 4. Strict Hallucination Fallback Test
    print("\n--- 4. STRICT HALLUCINATION FALLBACK TEST ---")
    unknown_res = await generate_response("What is the quantum teleportation frequency of Jupiter campus?", [])
    exact_fallback = "I could not find this information in the uploaded university documents."
    fallback_ok = unknown_res.get("answer") == exact_fallback
    print(f"Response: '{unknown_res.get('answer')}'")
    print(f"[{'PASS' if fallback_ok else 'FAIL'}] Output matches strict fallback string exactly.")
    results.append(("Strict Hallucination Fallback", fallback_ok))

    # 5. SOP Style Counselor Output Test
    print("\n--- 5. SOP STYLE COUNSELOR SYNTHESIS TEST ---")
    hostel_res = await generate_response("Explain hostel admission procedure", [])
    ans = hostel_res.get("answer")
    has_structure = any(heading in ans for heading in ["###", "**", "1.", "- "])
    print(f"Answer Format Sample:\n{ans[:200]}...\n")
    print(f"[{'PASS' if has_structure else 'FAIL'}] Structured SOP style answer generated (headings/lists/notes).")
    results.append(("SOP Style Counselor Synthesis", has_structure))

    # Summary Table
    print("\n================================================================")
    print("PHASE 13 TEST RESULTS SUMMARY")
    print("================================================================")
    all_ok = True
    for name, ok in results:
        print(f"- {name}: {'PASSED' if ok else 'FAILED'}")
        if not ok:
            all_ok = False
    print(f"\nOVERALL STATUS: {'SUCCESS' if all_ok else 'FAILURE'}")

if __name__ == "__main__":
    asyncio.run(run_phase13_tests())
