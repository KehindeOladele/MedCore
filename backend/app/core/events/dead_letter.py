from datetime import datetime, timezone
from app.core.supabase_admin import supabase_admin


# -----------------------------
# MOVE EVENT TO DLQ
# -----------------------------
def move_to_dead_letter(event: dict, reason: str):

    supabase_admin.table("events_dead_letter").insert({
        "id": event["id"],
        "original_event_id": event["id"],
        "aggregate_type": event.get("aggregate_type"),
        "aggregate_id": event.get("aggregate_id"),
        "event_type": event.get("event_type"),
        "payload": event.get("payload"),

        "retry_count": event.get("retry_count", 0),
        "failure_reason": reason,

        "failed_at": datetime.now(timezone.utc).isoformat()
    }).execute()