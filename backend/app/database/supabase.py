from functools import lru_cache

from supabase import Client, create_client

from app.config import settings


@lru_cache
def get_supabase_client() -> Client:
    """
    Returns a cached Supabase client using the service role key.
    Used for admin operations, database queries, and storage access.
    """
    return create_client(settings.supabase_url, settings.supabase_service_key)


@lru_cache
def get_supabase_anon_client() -> Client:
    """
    Returns a cached Supabase client using the anon key.
    Used for public-facing operations that respect Row Level Security.
    """
    return create_client(settings.supabase_url, settings.supabase_anon_key)
