"""
Triggers batched reingest on live Vercel backend.
Calls /admin/reingest-batch 3 times to index all 14 PDFs.
"""
import httpx
import time

BASE = "https://nexora-backend-three.vercel.app/api/v1"
TOKEN = "dev-token-admin-session-xyz"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

batches = [
    {"start": 0, "end": 5, "clear": True},
    {"start": 5, "end": 10, "clear": False},
    {"start": 10, "end": 14, "clear": False},
]

total_vectors = 0

for batch in batches:
    print(f"\nBatch {batch['start']}-{batch['end']}...")
    try:
        url = f"{BASE}/admin/reingest-batch?start={batch['start']}&end={batch['end']}&clear={str(batch['clear']).lower()}"
        r = httpx.post(url, headers=HEADERS, timeout=120)
        print(f"  Status: {r.status_code}")
        data = r.json()
        print(f"  Vectors this batch: {data.get('total_vectors', 0)}")
        for res in data.get("results", []):
            status = res.get("status", "?")
            chunks = res.get("chunks", 0)
            err = res.get("error", "")
            print(f"    {res['file']}: {status} ({chunks} chunks) {err}")
        total_vectors += data.get("total_vectors", 0)
    except Exception as e:
        print(f"  Error: {e}")
    
    if batch != batches[-1]:
        print("  Waiting 5s before next batch...")
        time.sleep(5)

print(f"\nAll batches done. Total vectors indexed: {total_vectors}")

# Check final stats
print("\nFinal Pinecone stats:")
r = httpx.get(f"{BASE}/admin/pinecone-stats", headers=HEADERS, timeout=15)
print(r.text)
