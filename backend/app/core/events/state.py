from datetime import datetime, timezone
from app.core.supabase_admin import supabase_admin
from app.core.events.schemas import EventStatus
from app.core.events.constants import MAX_RETRIES
from app.core.events.backoff import compute_next_retry_at


# ----- Event Processed Sucessful -----
def mark_processed(event_id: str):

    (
        supabase_admin
        .table("events")
        .update({
            "status": EventStatus.PROCESSED,
            "processed_at":
                datetime.now(
                    timezone.utc
                ).isoformat()
        })
        .eq("id", event_id)
        .execute()
    )


# ----- Event Processed Failed -----
def mark_failed(event_id: str, reason: str):

    event = (
        supabase_admin
        .table("events")
        .select("retry_count")
        .eq("id", event_id)
        .single()
        .execute()
    ).data

    retry_count = (event.get("retry_count") or 0) + 1 if isinstance(event, dict) else 1
    retry_count = int(retry_count)

    if retry_count >= MAX_RETRIES:
        status = EventStatus.DEAD
        next_retry_at = None
    else:
        status = EventStatus.FAILED
        next_retry_at = compute_next_retry_at(retry_count)

    (
        supabase_admin
        .table("events")
        .update({
            "retry_count": retry_count,
            "status": status,
            "last_error": reason,
            "next_retry_at": next_retry_at,
            "processed_at": datetime.now(timezone.utc).isoformat()
        })
        .eq("id", event_id)
        .execute()
    )