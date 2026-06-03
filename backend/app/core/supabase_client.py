from supabase import create_client, Client
from app.core.config import settings


# ---- Public / User-scoped Supabase Client ----
if settings.SUPABASE_URL is None:
    raise ValueError("SUPABASE_URL is required")
if settings.SUPABASE_PUBLISHABLE_KEY is None:
    raise ValueError("SUPABASE_PUBLISHABLE_KEY is required")

supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_PUBLISHABLE_KEY,
)

# Logging output of Supabase Client
print("SUPABASE_URL:", settings.SUPABASE_URL)

print(
    "PUBLISHABLE KEY PREFIX:",
    settings.SUPABASE_PUBLISHABLE_KEY[:20]
    if settings.SUPABASE_PUBLISHABLE_KEY
    else None
)