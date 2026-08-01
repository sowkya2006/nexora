"""
Trigger reingest-from-storage on live Vercel backend.
Fetches PDFs from Supabase Storage and re-indexes with HF API embeddings.
"""
import httpx
import time

BASE = "https://nexora-backend-three.vercel.app/api/v1"
H = {"Authorization": "Bearer dev-token-admin-session-xyz"}

batches = [
    {"start": 0, "end": 5, "clear": True},
    {"start": 5, "end": 10, "clear": False},
    {"start": 10, "end": 14, "clear": False},
]

total = 0
for batch in batches:
    print(f"\nBatch {batch['start']}-{batch['end']} (clear={batch['clear']})...")
    url = f"{BASE}/admin/reingest-from-storage"
    params = {"start": batch["start"], "end": batch["end"], "clear": str(batch["clear"]).lower()}
    try:
        r = httpx.post(url, params=params, headers=H, timeout=120)
        data = r.json()
        print(f"  Status: {r.status_code}")
        print(f"  Vectors this batch: {data.get('total_vectors_this_batch', 0)}")
        for res in data.get("results", []):
            st = res.get("status", "?")
            ch = res.get("chunks", 0)
            err = res.get("error", "")
            print(f"    {res['file']}: {st} ({ch} chunks) {err[:80] if err else ''}")
        total += data.get("total_vectors_this_batch", 0)
    except Exception as e:
        print(f"  Error: {e}")

    if batch != batches[-1]:
        print("  Waiting 5s...")
        time.sleep(5)

print(f"\nTotal vectors indexed: {total}")

# Check final Pinecone stats
print("\nFinal Pinecone stats:")
r = httpx.get(f"{BASE}/admin/pinecone-stats", headers=H, timeout=15)
print(r.text)

# Quick chat test
print("\nTesting chat...")
r = httpx.post(f"{BASE}/chat/query",
               json={"question": "What are the hostel facilities?", "session_id": "final-test", "history": []},
               timeout=60)
print("Chat response:", r.text[:300])
