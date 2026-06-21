from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.core.events.monitoring import (
    get_events,
    get_event,
    get_event_stats,
    get_failed_events,
    get_dead_letter_events
)


router = APIRouter(prefix="/admin/events", tags=["Event Monitoring"])


# -----------------------------
# LIST EVENTS
# -----------------------------
@router.get("")
def list_events(
    status: str | None = None,
    limit: int = 100,
    user=Depends(get_current_user)
):
    return get_events(status, limit)


# -----------------------------
# EVENT DETAIL
# -----------------------------
@router.get("/{event_id}")
def event_detail(
    event_id: str,
    user=Depends(get_current_user)
):
    return get_event(event_id)


# -----------------------------
# STATS
# -----------------------------
@router.get("/stats")
def stats(user=Depends(get_current_user)):
    return get_event_stats()


# -----------------------------
# FAILED EVENTS
# -----------------------------
@router.get("/failed")
def failed(user=Depends(get_current_user)):
    return get_failed_events()


# -----------------------------
# DEAD LETTER EVENTS
# -----------------------------
@router.get("/dead")
def dead(user=Depends(get_current_user)):
    return get_dead_letter_events()