from app.core.supabase_admin import supabase_admin
from app.core.config import settings
import logging


logger = logging.getLogger(__name__)


# ----- Event Based Emitter infrastructure -----
def emit_event(
    aggregate_type: str,
    aggregate_id: str,
    event_type: str,
    payload: dict | None = None
):
    
    logger.info("EMIT EVENT START")
    logger.info(f"EVENT TYPE: {event_type}")
    logger.info(f"SUPABASE URL: {settings.SUPABASE_URL}")
    logger.info(
        f"SECRET KEY PREFIX: {settings.SUPABASE_SECRET_KEY[:20]}"
    )

    result= (
        supabase_admin
        .table("events")
        .insert({
            "aggregate_type": aggregate_type,
            "aggregate_id": aggregate_id,
            "event_type": event_type,
            "payload": payload or {}
        })
        .execute()
    )

    logger.info(
        "Emitted event %s (%s)",
        event_type,
        aggregate_id
    )

    return result