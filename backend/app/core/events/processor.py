import logging
from datetime import datetime, timezone
from typing import Any, cast

from app.core.supabase_admin import supabase_admin
from app.core.events.dispatcher import dispatch_event
from app.core.events.locking import (
    acquire_event_lock,
    recover_stuck_events,
    requeue_failed_events,
)
from app.core.events.state import (
    mark_processed,
    mark_failed,
)
from app.core.events.constants import BATCH_SIZE


logger = logging.getLogger(__name__)


# ----- MAIN EVENT PROCESSOR -----
def process_pending_events():

    # 1. Cleanup stuck events (processing -> pending fallback)
    recover_stuck_events()

    # 2. Retry failed events that are eligible again
    requeue_failed_events()

    # 3. Fetch candidate events (DO NOT filter next_retry_at here)
    events = cast(
        list[dict[str, Any]],
        (
            supabase_admin
            .table("events")
            .select("*")
            .in_("status", ["pending", "failed"])
            .order("created_at")
            .limit(BATCH_SIZE)
            .execute()
        ).data
    )

    logger.info("Found %s candidate events", len(events))

    now = datetime.now(timezone.utc).isoformat()

    # PROCESS LOOP
    for event in events:

        event_id = event["id"]

        # 1. Skip retry-scheduled events
        next_retry_at = event.get("next_retry_at")
        if next_retry_at and next_retry_at > now:
            continue

        # 2. Skip maxed-out retries (safety net)
        if event.get("retry_count", 0) >= event.get("max_retries", 3):
            logger.warning("Event %s reached max retries", event_id)
            continue

        # 3. Acquire lock (critical for concurrency safety)
        locked = acquire_event_lock(event_id)

        if not locked:
            continue

        logger.info(
            "Processing event %s (%s)",
            event_id,
            event.get("event_type"),
        )

        try:
            # 4. Dispatch to handler
            dispatch_event(event)

            # 5. Mark success
            mark_processed(event_id)

        except Exception as e:

            logger.exception(
                "Failed processing event %s",
                event_id,
            )

            # 6. Mark failure + schedule retry/DLQ inside state layer
            mark_failed(
                event_id,
                reason=f"{type(e).__name__}: {str(e)}",
            )


# ----- OPTIONAL DEBUG QUERY HELPERS -----
def fetch_pending_events():
    """
    Debug helper (not used in main loop anymore)
    """
    return (
        supabase_admin
        .table("events")
        .select("*")
        .eq("status", "pending")
        .limit(BATCH_SIZE)
        .execute()
        .data
    )


def should_process(event: dict[str, Any]) -> bool:
    """
    Phase 3 scheduling gate (optional reuse elsewhere)
    """
    now = datetime.now(timezone.utc).isoformat()

    next_retry_at = event.get("next_retry_at")

    if not next_retry_at:
        return True

    return next_retry_at <= now