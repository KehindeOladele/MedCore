from datetime import datetime, timezone
from app.core.supabase_admin import supabase_admin
from app.core.audit.service import log_audit_event
from app.core.audit.actions import AuditActions

# -----------------
# REPLAY DEAD EVENT
# -----------------
def replay_dead_event(
    dead_event_id: str,
    actor_id: str
):
    dead_event = (
        supabase_admin
        .table("events_dead_letter")
        .select("*")
        .eq("id", dead_event_id)
        .single()
        .execute()
    ).data

    if not dead_event:
        raise ValueError(
            f"Dead event {dead_event_id} not found"
        )

    if dead_event.get("replayed"):
        raise ValueError(
            "Event already replayed"
        )

    new_event = (
        supabase_admin
        .table("events")
        .insert({
            "aggregate_type":
                dead_event["aggregate_type"],

            "aggregate_id":
                dead_event["aggregate_id"],

            "event_type":
                dead_event["event_type"],

            "payload":
                dead_event["payload"],

            "status": "pending",

            "retry_count": 0,

            "next_retry_at": None
        })
        .execute()
    ).data[0]

    (
        supabase_admin
        .table("events_dead_letter")
        .update({
            "replayed": True,
            "replayed_at":
                datetime.now(
                    timezone.utc
                ).isoformat(),
            "replayed_by": actor_id
        })
        .eq("id", dead_event_id)
        .execute()
    )

    log_audit_event(
        actor_id=actor_id,
        actor_type="admin",
        action=AuditActions.EVENT_REPLAYED,
        resource_type="event",
        resource_id=new_event["id"],
        metadata={
            "dead_event_id": dead_event_id,
            "original_event_id":
                dead_event["original_event_id"]
        }
    )

    return {
        "message": "Event replayed successfully",
        "new_event_id": new_event["id"]
    }