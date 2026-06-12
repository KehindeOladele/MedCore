from datetime import datetime, timezone
from app.core.supabase_admin import supabase_admin
from app.core.events.schemas import EventStatus
from app.core.events.constants import MAX_RETRIES


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
def mark_failed(
    event_id: str,
    reason: str
):

    event = (
        supabase_admin
        .table("events")
        .select("retry_count")
        .eq("id", event_id)
        .single()
        .execute()
    ).data

    current_retry_count = event.get(
        "retry_count", 0
    )

    new_retry_count = (
        current_retry_count + 1
    )

    status = (
        EventStatus.DEAD
        if new_retry_count >= MAX_RETRIES
        else EventStatus.FAILED
    )

    (
        supabase_admin
        .table("events")
        .update({
            "status": status,
            "retry_count": new_retry_count,
            "failure_reason": reason,
            "last_attempt_at":
                datetime.now(
                    timezone.utc
                ).isoformat()
        })
        .eq("id", event_id)
        .execute()
    )