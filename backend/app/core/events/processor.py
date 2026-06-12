from datetime import datetime, timezone
from typing import Any, cast
from app.core.supabase_admin import supabase_admin
from app.core.events.dispatcher import dispatch_event
from app.core.events.locking import (
    acquire_event_lock,
    recover_stuck_events,
    requeue_failed_events
)
from app.core.events.state import (
    mark_processed, 
    mark_failed
)
from app.core.events.constants import (
    MAX_RETRIES,
    BATCH_SIZE
)


# ----- Event Processor -----
def process_pending_events():

    recover_stuck_events()

    requeue_failed_events()

    events = cast(list[dict[str, Any]], (
        supabase_admin
        .table("events")
        .select("*")
        .eq("status", "pending")
        .order("created_at")
        .limit(BATCH_SIZE)
        .execute()
    ).data)
    

    for event in events:
        if (
            event.get("retry_count", 0)
            >= MAX_RETRIES
        ):
            continue

        locked = acquire_event_lock(
            event["id"]
        )

        if not locked:
            continue
            
        try:    
            dispatch_event(event)
            mark_processed(event["id"])

        except Exception as e:
            mark_failed(
                event["id"],
                reason= f"{type(e).__name__}: {str(e)}"
            )