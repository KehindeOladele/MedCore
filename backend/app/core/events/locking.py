from datetime import datetime, timezone, timedelta
from app.core.supabase_admin import supabase_admin
from app.core.events.schemas import EventStatus


# ----- Event Lock -----
def acquire_event_lock(event_id: str) -> bool:
    """
    Prevents duplicate processing when multiple 
    background tasks run at the same time.
    """
    now = datetime.now(timezone.utc).isoformat()
    result = (
        supabase_admin
        .table("events")
        .update({
            "status": EventStatus.PROCESSING,
            "locked_at": now
        })
        .eq("id", event_id)
        .eq("status", EventStatus.PENDING)
        .execute()
    )

    return (
        bool(result.data)
        and len(result.data) == 1
    )


# ----- Stuck Process Recovery -----
def recover_stuck_events():

    cutoff = (
        datetime.now(timezone.utc)
        - timedelta(
            minutes=5
        )
    ).isoformat()

    (
        supabase_admin
        .table("events")
        .update({
            "status": EventStatus.PENDING
        })
        .eq(
            "status",
            EventStatus.PROCESSING
        )
        .lt(
            "locked_at",
            cutoff
        )
        .execute()
    )