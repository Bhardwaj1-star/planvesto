from supabase import Client, create_client

from config.settings import SUPABASE_SERVICE_ROLE_KEY, SUPABASE_URL

_client: Client | None = None


def get_supabase() -> Client:
    global _client
    if _client is None:
        _client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    return _client
