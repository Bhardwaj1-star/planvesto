"""Supabase client bridge preserving legacy get_supabase() signature."""

from app.infrastructure.providers.supabase.client import get_supabase_client, Client

# Maintain legacy get_supabase accessor
get_supabase = get_supabase_client

__all__ = ["get_supabase", "Client"]
