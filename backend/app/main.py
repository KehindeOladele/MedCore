from fastapi import FastAPI
from app.modules.auth.router import router as auth_router
from app.modules.patients.router import router as patients_router
from app.modules.records.router import router as records_router
from app.modules.dashboard.router import router as dashboard_router
from app.modules.medical_history.router import router as medical_history_router
from app.modules.laboratory.router import router as laboratory_router
from app.modules.organizations.router import router as org_router


# ===== Initialize FastAPI Application =====
app = FastAPI(title="MedCore API", version="1.0.0", description="API for Electronic Medical History System")


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
