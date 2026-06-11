from datetime import datetime, timezone
from typing import Any, cast
from app.core.supabase_admin import supabase_admin
from app.core.events.dispatcher import dispatch_event
from app.core.events.locking import acquire_event_lock
from app.core.events.state import mark_processed, mark_failed


MAX_RETRIES = 3

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
                str(e)
            )