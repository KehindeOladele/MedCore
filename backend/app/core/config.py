import os
from dotenv import load_dotenv

load_dotenv()


# --- Environment Settings ---
class Settings:
    # Environment
    ENV: str = os.getenv("ENV", "development")

# ----- Supabase Configuration -----
    # 1. Supabase PRoject URL
    SUPABASE_URL: str = os.getenv("SUPABASE_URL").strip()
    # 2. Public/User-scoped
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY").strip() # SUPABASE_KEY : Client-side (browser/mobile)
    # 3. Backend/Admin-scoped
    SUPABASE_SECRET_KEY: str = os.getenv("SUPABASE_SECRET_KEY").strip() # SUPABASE_SECRET_KEY: Server-side (Edge Functions / your backend only)

    # ----- Security -----
    JWT_AUDIENCE: str = os.getenv("JWT_AUDIENCE", "authenticated")

    # ---- Validating Required Settings ----
    def validate(self):
        missing = []

        required = {
            "SUPABASE_URL": self.SUPABASE_URL,
            "SUPABASE_KEY": self.SUPABASE_KEY,
            "SUPABASE_SECRET_KEY": self.SUPABASE_SECRET_KEY,
        }

        for key, value in required.items():
            if not value:
                missing.append(key)

        if missing:
            raise RuntimeError(
                f"Missing required environment variables: "
                f"{', '.join(missing)}"
            )

# ----- Instantiate and Validate Settings -----
settings = Settings()
settings.validate()
