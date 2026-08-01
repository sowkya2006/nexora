import httpx

BASE = "https://nexora-backend-three.vercel.app/api/v1"
H = {"Authorization": "Bearer dev-token-admin-session-xyz"}

# Check Pinecone stats
r = httpx.get(f"{BASE}/admin/pinecone-stats", headers=H, timeout=15)
print("Pinecone stats:", r.text)

# Test query
r = httpx.post(
    f"{BASE}/admin/test-query",
    params={"q": "What are the hostel facilities?"},
    headers=H,
    timeout=60
)
print("\nTest query result:", r.text[:1000])
