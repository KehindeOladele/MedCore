from supabase import create_client, Client
from app.core.config import settings


# ---- Public / User-scoped Supabase Client ----
supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_PUBLISHABLE_KEY
)