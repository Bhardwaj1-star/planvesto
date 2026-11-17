"""Supabase provider client and identity adapters."""

from app.infrastructure.providers.supabase.client import get_supabase_client, SupabaseClientFactory

__all__ = ["get_supabase_client", "SupabaseClientFactory"]
