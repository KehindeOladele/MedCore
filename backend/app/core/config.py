import os
from dotenv_vault import load_dotenv

load_dotenv()


# --- Environment Settings ---
class Settings:
    # Environment
    ENV: str = os.getenv("ENV", "development")

# ----- Supabase Configuration -----
    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    # ----- Security -----
    JWT_AUDIENCE: str = os.getenv("JWT_AUDIENCE", "authenticated")

    # ---- Validating Required Settings ----
    def validate(self):
        missing = []
        if not self.SUPABASE_URL:
            missing.append("SUPABASE_URL")
        if not self.SUPABASE_SERVICE_ROLE_KEY:
            missing.append("SUPABASE_SERVICE_ROLE_KEY")

        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

# ----- Instantiate and Validate Settings -----
settings = Settings()
settings.validate()
