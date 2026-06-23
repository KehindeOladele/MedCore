from fastapi import (
    APIRouter, 
    Depends,
    Query
)
from app.core.security import get_current_user
from app.core.events.monitoring import (
    get_events,
    get_event,
    get_event_stats,
    get_failed_events,
    get_dead_letter_events,
    get_dead_letter_event
)


router = APIRouter(prefix="/admin/events", tags=["Event Monitoring"])


# -----------------------------
# LIST EVENTS
# -----------------------------
@router.get("")
def list_events(
    status: str | None = None,
    limit: int = Query(
        default=100,
        ge=1,
        le=500
    ),
    user=Depends(get_current_user)
):
    return get_events(status, limit)


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
def failed(
    limit: int = Query(
        default=100,
        ge=1,
        le=500
    ),
    user=Depends(get_current_user)
    ):
    return get_failed_events(limit)


# -----------------------------
# DEAD LETTER EVENTS
# -----------------------------
@router.get("/dead")
def dead(
    
    limit: int = Query(
        default=100,
        ge=1,
        le=500
    ),
    user=Depends(get_current_user)
    ):
    return get_dead_letter_events(limit)


# -----------------------------
# EVENT DETAIL
# -----------------------------
@router.get("/{event_id}")
def event_detail(
    event_id: str,
    user=Depends(get_current_user)
):
    return get_event(event_id)


# ------------------------------
# GET DEAD EVENT DETAIL
# ------------------------------
@router.get("/dead/{dead_event_id}")
def dead_event_detail(
    dead_event_id: str,
    user=Depends(get_current_user)
):
    return get_dead_letter_event(
        dead_event_id
    )