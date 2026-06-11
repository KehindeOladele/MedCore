from datetime import datetime, timezone
from app.core.supabase_admin import supabase_admin
from app.core.events.schemas import EventStatus


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

    (
        supabase_admin
        .table("events")
        .update({
            "status": EventStatus.FAILED,
            "failure_reason": reason,
            "retry_count":
                event.get(
                    "retry_count",
                    0
                ) + 1,
            "last_attempt_at":
                datetime.now(
                    timezone.utc
                ).isoformat()
        })
        .eq("id", event_id)
        .execute()
    )