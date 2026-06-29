from app.core.events.dispatcher import register
from app.core.events.schemas import EventTypes
from app.core.events.emitter import emit_event

from app.modules.organizations.queries import (
    get_organization,
)


# ---------------------------------------
# Organization Created Handler
# ---------------------------------------
@register(EventTypes.ORGANIZATION_CREATED)
def handle_organization_created(event):

    organization_id = event["aggregate_id"]

    emit_event(
        aggregate_type="organization",
        aggregate_id=organization_id,
        event_type=EventTypes.ORGANIZATION_ONBOARDING_REQUESTED,
        payload=event.get("payload", {})
    )


# ------------------------------------------
# Organization Onboarding Handler
# ------------------------------------------
@register(EventTypes.ORGANIZATION_ONBOARDING_REQUESTED)
def handle_organization_onboarding(event):

    organization_id = event["aggregate_id"]

    organization = get_organization(
        organization_id
    )

    payload = event.get("payload", {})