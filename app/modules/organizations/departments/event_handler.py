from app.core.events.registry import register
from app.core.events.schemas import EventTypes
from app.core.events.emitter import emit_event



# -------------------------
# Create Department Event
# -------------------------
@register(EventTypes.DEPARTMENT_CREATED)
def handle_department_created(event):
    _forward_event(
        aggregate_type="department",
        aggregate_id=event["aggregate_id"],
        event_type=EventTypes.DEPARTMENT_ONBOARDING_REQUESTED,
        payload=event.get("payload", {}),
    )

# --------------------------
# Update Departments Event
# --------------------------
@register(EventTypes.DEPARTMENT_UPDATED)
def handle_department_updated(event):
    """
    Handle department.updated events.
    """

    # Reserved for future consumers:
    #
    # - Search indexing
    # - Analytics
    # - Notifications
    # - Cache invalidation
    #
    return None


# -------------------------
# Delete Department Event
# -------------------------
@register(EventTypes.DEPARTMENT_DELETED)
def handle_department_deleted(event):
    """
    Handle department.deleted events.
    """

    # Reserved for future cleanup.
    return None


# ------------------------------------
# Department Onboarding Request Event
# ------------------------------------
@register(EventTypes.DEPARTMENT_ONBOARDING_REQUESTED)
def handle_department_onboarding_requested(event):
    """
    Begin department onboarding workflow.
    """

    emit_event(
        aggregate_type="department",
        aggregate_id=event["aggregate_id"],
        event_type=EventTypes.DEPARTMENT_ONBOARDING_COMPLETED,
        payload=event.get("payload", {}),
    )


# ------------------------------------
# Department Onboarding Complete Event
# ------------------------------------
@register(EventTypes.DEPARTMENT_ONBOARDING_COMPLETED)
def handle_department_onboarding_completed(event):
    """
    Complete department onboarding workflow.
    """

    # Reserved for Setup Wizard integration.    
    return None


# --------------------
# Forward Logic Helper
# --------------------
def _forward_event(
    *,
    aggregate_type: str,
    aggregate_id: str,
    event_type: str | EventTypes,
    payload: dict,
) -> None:
    emit_event(
        aggregate_type=aggregate_type,
        aggregate_id=aggregate_id,
        event_type=event_type,
        payload=payload,
    )