from datetime import datetime, timezone
from typing import Any, cast
from app.core.supabase_admin import supabase_admin
from app.core.events.dispatcher import dispatch_event


# ----- Event Processor -----
def process_pending_events():

    events = cast(list[dict[str, Any]], (
        supabase_admin
        .table("events")
        .select("*")
        .eq("status", "pending")
        .order("created_at")
        .execute()
    ).data)

    for event in events:
        try:
            dispatch_event(event)
            (
                supabase_admin
                .table("events")
                .update({
                    "status": "processed",
                    "processed_at":
                        datetime.now(
                            timezone.utc
                        ).isoformat()
                })
                .eq("id", event["id"])
                .execute()
            )

        except Exception as e:
            (
                supabase_admin
                .table("events")
                .update({
                    "status": "failed",
                    "failure_reason": str(e),
                    "retry_count":
                        event.get("retry_count", 0) + 1,
                    "last_attempt_at":
                        datetime.now(
                            timezone.utc
                        ).isoformat()
                })
                .eq("id", event["id"])
                .execute()
            )