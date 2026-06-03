import os
from dotenv import load_dotenv
from typing import Optional
<<<<<<< HEAD
=======
from pydantic import EmailStr

>>>>>>> template

load_dotenv()


# --- Environment Settings ---
class Settings:
    # Environment
    ENV: str = os.getenv("ENV", "development")

<<<<<<< HEAD
# ----- Supabase Configuration -----
    # 1. Supabase PRoject URL
    SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
    # 2. Public/User-scoped
    SUPABASE_PUBLISHABLE_KEY: Optional[str] = os.getenv("SUPABASE_PUBLISHABLE_KEY")# SUPABASE_KEY : Client-side (browser/mobile)
    # 3. Backend/Admin-scoped
    SUPABASE_SECRET_KEY: Optional[str] = os.getenv("SUPABASE_SECRET_KEY") # SUPABASE_SECRET_KEY: Server-side (Edge Functions / your backend only)
=======
    # ----- Supabase Configuration -----
    # 1. Supabase PrRoject URL
    SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
    # 2. Public/User-scoped
    SUPABASE_PUBLISHABLE_KEY: Optional[str] = os.getenv("SUPABASE_PUBLISHABLE_KEY") # SUPABASE_PUBLISHABLE_KEY : Client-side (browser/mobile)
    # 3. Backend/Admin-scoped
    SUPABASE_SECRET_KEY: Optional[str] = os.getenv("SUPABASE_SECRET_KEY") # SUPABASE_SECRET_KEY: Server-side (Edge Functions / your backend only)
    
    # ----- Resend Configuration -----
    # 4. Resend API
    RESEND_API_KEY: Optional[str] = os.getenv("RESEND_API_KEY")
    # 5. Email From
    EMAIL_FROM: Optional[EmailStr] = os.getenv("EMAIL_FROM")
    # 6. Email Reply to
    EMAIL_REPLY_TO: Optional[EmailStr] = os.getenv("EMAIL_REPLY_TO")
    # 7. App Name
    APP_NAME: Optional[str] = os.getenv("APP_NAME")
    # 8. App Frontend URL
    FRONTEND_URL: Optional[str] = os.getenv("FRONTEND_URL")
>>>>>>> template

    # ----- Security -----
    JWT_AUDIENCE: str = os.getenv("JWT_AUDIENCE", "authenticated")

    # ---- Validating Required Settings ----
    def validate(self):
        missing = []

        required = {
            "SUPABASE_URL": self.SUPABASE_URL,
            "SUPABASE_PUBLISHABLE_KEY": self.SUPABASE_PUBLISHABLE_KEY,
            "SUPABASE_SECRET_KEY": self.SUPABASE_SECRET_KEY,
            "RESEND_API_KEY": self.RESEND_API_KEY,
            "EMAIL_FROM": self.EMAIL_FROM,
            "APP_NAME": self.APP_NAME,
            "FRONTEND_URL": self.FRONTEND_URL
        }

        for key, value in required.items():
            if value is None or value == "":
                missing.append(key)

        if missing:
            raise RuntimeError(
                f"Missing required environment variables: "
                f"{', '.join(missing)}"
            )

# ----- Instantiate and Validate Settings -----
settings = Settings()
settings.validate()
