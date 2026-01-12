from fastapi import FastAPI
from app.modules.auth.router import router as auth_router


# ----- Initialize FastAPI Application -----
app = FastAPI(title="MedCore API")


# ----- Include Routers -----
app.include_router(auth_router)


# ----- Health Check Endpoint -----
@app.get("/health")
def health():
    return {"status": "ok"}
