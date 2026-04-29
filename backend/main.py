import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.supabase_client import supabase
from app.modules.auth.router import router as auth_router
from app.modules.patients.router import router as patients_router
from app.modules.records.router import router as records_router
from app.modules.dashboard.router import router as dashboard_router
from app.modules.medical_history.router import router as medical_history_router
from app.modules.laboratory.router import router as laboratory_router
from app.modules.organizations.router import router as org_router


# ===== Initialize FastAPI Application =====
app = FastAPI(title="MedCore API", version="1.0.0", description="API for Electronic Medical History System")


# ===== CORS Middleware Configuration =====
# Example env var on Render:
# ALLOWED_ORIGINS= https://your-frontend.com,http://localhost:3000
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
allowed_origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]

# For local/dev convenience (optional):
if os.getenv("ENV", "development") == "development":
    allowed_origins += [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins else ["*"],  # Avoid "*" in production if possible
    allow_credentials=True,  # Needed if using cookies; okay with auth headers too
    allow_methods=["*"],
    allow_headers=["*"],
)



# ===== Include Routers =====


#  ===== Core Modules =====
# Auth Router
app.include_router(auth_router)
# Patients Router
app.include_router(patients_router)
# Records Router
app.include_router(records_router)
# Organization Router
app.include_router(org_router)


# ===== Feature Modules =====
# Medical History Router
app.include_router(medical_history_router)
# Laboratory Router
app.include_router(laboratory_router)


# ===== Aggregation Layer =====
app.include_router(dashboard_router)

# ----- Health Check Endpoint -----
@app.get("/health")
def health():
    return {"status": "ok"}
