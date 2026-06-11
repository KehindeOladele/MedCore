from fastapi import APIRouter
from app.core.supabase_admin import supabase_admin
from app.core.events.service import EventService
from app.core.events.processor import process_pending_events

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

# ----- Admin Event Monitoring Endpoint -----
@router.get("/events")
def get_events(
    limit: int= 100
):

    return (
        supabase_admin
        .table("events")
        .select("*")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
        .data
    )


# ----- Get Failed Events Endpoint -----
@router.get("/failed")
def get_failed_events():

    return (
        supabase_admin
        .table("events")
        .select("*")
        .in_(
            "status",
            ["failed", "dead"]
        )
        .order("created_at", desc=True)
        .execute()
        .data
    )


# ----- Get Events by ID Endpoint -----
@router.get("/{event_id}")
def get_event(
    event_id: str
):

    return (
        supabase_admin
        .table("events")
        .select("*")
        .eq("id", event_id)
        .single()
        .execute()
        .data
    )


# 
@router.get("/metrics/summary")
def event_metrics():

    events = (
        supabase_admin
        .table("events")
        .select("status")
        .execute()
    ).data

    summary = {
        "pending": 0,
        "processing": 0,
        "processed": 0,
        "failed": 0,
        "dead": 0
    }

    for event in events:
        # guard against unexpected types (None, bool, etc.)
        if not isinstance(event, dict):
            continue

        status = event.get("status")
        if not isinstance(status, str):
            continue

        if status in summary:
            summary[status] += 1

    return summary


# ----- Event Retry Endpoint -----
@router.post("/{event_id}/retry")
def retry_event(
    event_id: str
):

    EventService.retry_event(
        event_id
    )

    process_pending_events()

    return {
        "message": "Event queued for retry"
    }


# ----- All Failed Event Retry Endpoint ----- 
@router.post("/retry-failed")
def retry_failed_events():
    failed_events = (
        supabase_admin
        .table("events")
        .select("id")
        .in_(
            "status",
            ["failed"]
        )
        .execute()
    ).data

    retried = 0

    for event in failed_events or []:
        if not isinstance(event, dict):
            continue

        event_id = event.get("id")
        if not isinstance(event_id, str):
            continue

        EventService.retry_event(event_id)
        retried += 1

    process_pending_events()

    return {
        "retried": retried
    }


# ----- Onboarding Event Monitoring Endpoint -----
@router.get("/onboarding")
def onboarding_events():
    return (
        supabase_admin
        .table("events")
        .select("*")
        .ilike(
            "event_type",
            "onboarding.%"
        )
        .order("created_at", desc=True)
        .execute()
        .data
    )