from supabase import create_client, Client
from app.core.config import settings


# ---- Admin Supabase Client ----
if settings.SUPABASE_URL is None:
    raise ValueError("SUPABASE_URL is required")
if settings.SUPABASE_SECRET_KEY is None:
    raise ValueError("SUPABASE_SECRET_KEY is required")

supabase_admin: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SECRET_KEY
)

# Logging output of Supabase Admin
print("SUPABASE_URL:", settings.SUPABASE_URL)

print(
    "PUBLISHABLE ADMIN KEY PREFIX:",
    settings.SUPABASE_SECRET_KEY[:20]
    if settings.SUPABASE_SECRET_KEY
    else None
)