from fastapi import FastAPI
from app.modules.auth.router import router as auth_router
from app.modules.patients.router import router as patients_router


# ----- Initialize FastAPI Application -----
app = FastAPI(title="MedCore API")


# ----- Include Routers -----
app.include_router(auth_router)

# ---- Patients Router -----
app.include_router(patients_router)

# ----- Health Check Endpoint -----
@app.get("/health")
def health():
    return {"status": "ok"}
