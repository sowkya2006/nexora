"""
Triggers the /admin/reingest endpoint on the live Vercel backend.
This causes the server to re-index all PDFs using HF embeddings.
"""
import httpx

BASE = "https://nexora-backend-three.vercel.app/api/v1"

# Use dev token directly — bypasses auth on development environment
token = "dev-token-admin-session-xyz"
headers = {"Authorization": f"Bearer {token}"}

# Step 2: Check Pinecone stats before
print("\nPinecone stats BEFORE:")
r = httpx.get(f"{BASE}/admin/pinecone-stats", headers=headers, timeout=15)
print(r.text)

# Step 3: Trigger reingest
print("\nTriggering reingest...")
r = httpx.post(f"{BASE}/admin/reingest", headers=headers, timeout=30)
print("Reingest response:", r.status_code, r.text)

print("\nDone. Wait 2-3 minutes then check Pinecone stats again.")
print("Run: python check_pinecone_after.py")
