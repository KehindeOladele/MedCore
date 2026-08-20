from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.core.events.metrics import (
    get_event_metrics,
    get_onboarding_metrics
)


router = APIRouter(prefix="/admin/metrics", tags=["Event Metrics"])


# -----------------------------
# SYSTEM METRICS
# -----------------------------
@router.get("/events")
def event_metrics(user=Depends(get_current_user)):
    return get_event_metrics()


# -----------------------------
# ONBOARDING METRICS
# -----------------------------
@router.get("/onboarding")
def onboarding_metrics(user=Depends(get_current_user)):
    return get_onboarding_metrics()