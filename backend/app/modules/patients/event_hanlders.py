from app.core.events.emitter import emit_event
from app.core.events.schemas import EventTypes
from app.modules.patients.onboarding import send_onboarding_email


# ----- Patient Create Hanlder ----- 
def handle_patient_created(
    patient_id: str,
    email: str
):

    emit_event(
        aggregate_type="patient",
        aggregate_id=patient_id,
        event_type=EventTypes.ONBOARDING_EMAIL_REQUESTED,
        payload={
            "email": email
        }
    )

    handle_onboarding_email_requested(
        patient_id=patient_id
    )


# ----- Onboarding Email Request Handler -----
def handle_onboarding_email_requested(
    patient_id: str
):

    # existing send_onboarding_email logic

    send_onboarding_email(patient_id)

    emit_event(
        aggregate_type="patient",
        aggregate_id=patient_id,
        event_type=EventTypes.ONBOARDING_EMAIL_SENT
    )