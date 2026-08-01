"""
Nexora University - Backend Setup Script
Reads credentials from environment variables or .env file.
Run: python setup_backend.py
"""
import os
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY", "")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

if not SUPABASE_URL:
    print("ERROR: Set SUPABASE_URL in your .env file")
    exit(1)

from supabase import create_client
print("--- 1. Testing Supabase Connection ---")
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
print("Supabase client initialized successfully!")

print("\n--- 2. Creating Supabase Storage Bucket ('documents') ---")
try:
    buckets = supabase.storage.list_buckets()
    bucket_names = [b.name for b in buckets]
    print(f"Existing buckets: {bucket_names}")
    if "documents" not in bucket_names:
        supabase.storage.create_bucket("documents", options={"public": True})
        print("Created 'documents' bucket.")
    else:
        print("'documents' bucket already exists.")
except Exception as e:
    print(f"Storage setup error: {e}")

print("\nSetup complete.")
