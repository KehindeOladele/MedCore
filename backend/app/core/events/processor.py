import logging
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


logger = logging.getLogger(__name__)

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

    logger.info(
        "Found %s pending events",
        len(events)
    )
    

    for event in events:
        if event.get(
            "retry_count", 0
        ) >= MAX_RETRIES:

            continue

        locked = acquire_event_lock(
            event["id"]
        )

        if not locked:
            continue

        logger.info(
            "Processing event %s (%s)",
            event["id"],
            event["event_type"]
        )
            
        try:    
            dispatch_event(event)
            mark_processed(event["id"])

        except Exception as e:
            
            logger.exception(
                "Failed processing event %s",
                event["id"]
            )

            mark_failed(
                event["id"],
                reason= f"{type(e).__name__}: {str(e)}"
            )

# ----- Retrive Pending Events -----
def fetch_pending_events():
    now = datetime.now(timezone.utc).isoformat()

    response = (
        supabase_admin
        .table("events")
        .select("*")
        .eq("status", "pending")
        .or_(
            f"next_retry_at.is.null,next_retry_at.lte.{now}"
        )
        .limit(BATCH_SIZE)
        .execute()
    )

    return response.data


#  ----- Processor Safety Rule -----
def should_process(event):
    if event["status"] != "pending":
        return False

    next_retry_at = event.get("next_retry_at")

    if not next_retry_at:
        return True

    return next_retry_at <= datetime.now(timezone.utc).isoformat()