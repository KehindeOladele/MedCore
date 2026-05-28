from supabase import create_client, Client
from app.core.config import settings


# ---- Admin Supabase Client ----
supabase_admin: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SECRET_KEY
)