"""
Nexora University - Verify All Services
Reads credentials from environment variables or .env file.
Run: python verify_all.py
"""
import os
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

print("--- 1. Testing Pinecone Connection ---")
try:
    from pinecone import Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)
    indexes = pc.list_indexes()
    print(f"Connected to Pinecone! Indexes: {[i.name for i in indexes]}")
except Exception as e:
    print(f"Pinecone error: {e}")

print("\n--- 2. Testing Supabase Connection ---")
try:
    from supabase import create_client
    sb = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    print("Supabase connected.")
except Exception as e:
    print(f"Supabase error: {e}")

print("\n--- 3. Testing Groq ---")
try:
    import httpx
    r = httpx.get("https://api.groq.com/openai/v1/models",
                  headers={"Authorization": f"Bearer {GROQ_API_KEY}"}, timeout=10)
    print(f"Groq API status: {r.status_code}")
except Exception as e:
    print(f"Groq error: {e}")

print("\nVerification complete.")
