"""Supabase client bridge preserving legacy get_supabase() signature."""

from supabase import Client
from app.infrastructure.providers.supabase.client import get_supabase_client

# Maintain legacy get_supabase accessor
get_supabase = get_supabase_client

__all__ = ["get_supabase", "Client"]
