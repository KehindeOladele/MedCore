from app.core.events.emitter import emit_event
from app.core.events.schemas import EventTypes
from app.core.events.registry import register
from app.core.events.emitter import emit_event
from app.core.events.schemas import EventTypes
from app.modules.patients.onboarding import send_onboarding_email



# ----- Patient Create Hanlder ----- 
@register(EventTypes.PATIENT_CREATED)
def handle_patient_created(event):

    emit_event(
        aggregate_type="patient",
        aggregate_id=event["aggregate_id"],
        event_type=EventTypes.ONBOARDING_EMAIL_REQUESTED,
        payload=event.get("payload", {})
    )

    handle_onboarding_email_requested(event)


# ----- Onboarding Email Request Handler -----
@register(EventTypes.ONBOARDING_EMAIL_REQUESTED)
def handle_onboarding_email_requested(event):

    patient_id = event["aggregate_id"]

    send_onboarding_email(patient_id)

    emit_event(
        aggregate_type="patient",
        aggregate_id=patient_id,
        event_type=EventTypes.ONBOARDING_EMAIL_SENT
    )