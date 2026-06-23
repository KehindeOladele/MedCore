from datetime import datetime, timezone
from fastapi import HTTPException
from app.core.supabase_admin import supabase_admin


# -----------------------------
# GET EVENTS (FILTERABLE)
# -----------------------------
def get_events(status: str | None = None, limit: int = 100):

    query = (
        supabase_admin
        .table("events")
        .select("*")
        .order("created_at", desc=True)
        .limit(limit)
    )

    if status:
        query = query.eq("status", status)

    return query.execute().data


# -----------------------------
# GET EVENT BY ID
# -----------------------------
def get_event(event_id: str):

    return (
        supabase_admin
        .table("events")
        .select("*")
        .eq("id", event_id)
        .single()
        .execute()
        .data
    )


# -----------------------------
# EVENT STATS (CORE HEALTH METRICS)
# -----------------------------
def get_event_stats():

    events = (
        supabase_admin
        .table("events")
        .select("status")
        .execute()
        .data
    )

    total = len(events)

    stats = {
        "total": total,
        "pending": 0,
        "processing": 0,
        "processed": 0,
        "failed": 0,
        "dead": 0,
    }

    for e in events:
        status = e.get("status")
        if status in stats:
            stats[status] += 1

    stats["success_rate"] = (
        stats["processed"] / total * 100
        if total > 0 else 0
    )

    return stats


# -----------------------------
# FAILED EVENTS
# -----------------------------
def get_failed_events(limit: int = 100):

    return (
        supabase_admin
        .table("events")
        .select("*")
        .eq("status", "failed")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
        .data
    )


# -----------------------------
# DEAD LETTER EVENTS
# -----------------------------
def get_dead_letter_events(limit: int = 100):

    return (
        supabase_admin
        .table("events_dead_letter")
        .select("*")
        .order("failed_at", desc=True)
        .limit(limit)
        .execute()
        .data
    )


# ------------------------
# GET DEAD LETTER EVENT ID
# ------------------------
def get_dead_letter_event(
    dead_event_id: str
):

    event = (
        supabase_admin
        .table("events_dead_letter")
        .select("*")
        .eq("id", dead_event_id)
        .single()
        .execute()
        .data
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Dead letter event not found"
        )

    return event