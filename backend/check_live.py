import httpx

url = "https://nexora-backend-three.vercel.app/api/v1/chat/query"
body = {"question": "What are the hostel facilities?", "session_id": "dbg-1", "history": []}

try:
    r = httpx.post(url, json=body, timeout=60)
    print("Status:", r.status_code)
    print("Response:", r.text[:1000])
except Exception as e:
    print("Error:", e)
