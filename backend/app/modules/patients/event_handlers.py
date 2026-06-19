from app.core.events.emitter import emit_event
from app.core.events.schemas import EventTypes
from app.core.events.registry import register
from app.modules.patients.onboarding import send_onboarding_email
from app.core.supabase_admin import supabase_admin
from app.core.events.service import EventService
import logging


logger= logging.getLogger(__name__)


# ----- Patient Create Hanlder ----- 
@register(EventTypes.PATIENT_CREATED)
def handle_patient_created(event):

    logger.info(
        f"HANDLER RECEIVED EVENT {event['event_type']} "
        f"FOR {event['aggregate_id']}"
    )
    print(
        f"HANDLER RECEIVED EVENT {event['event_type']} "
        f"FOR {event['aggregate_id']}"
    )

    EventService.patient_created(
        patient_id=event["aggregate_id"],
        email=event["payload"].get("email")
    )

    emit_event(
        aggregate_type="patient",
        aggregate_id=event["aggregate_id"],
        event_type=EventTypes.ONBOARDING_EMAIL_REQUESTED,
        payload=event["payload"]
    )


# ----- Onboarding Email Request Handler -----
@register(EventTypes.ONBOARDING_EMAIL_REQUESTED)
def handle_onboarding_email_requested(event):

    patient_id = event["aggregate_id"]
    
    patient = (
        supabase_admin
        .table("patients")
        .select("onboarding_email_sent")
        .eq("id", patient_id)
        .maybe_single()
        .execute()
    ).data

    logger.info(f"PATIENT LOOKUP RESULT: {patient}")
    print(f"PATIENT LOOKUP RESULT: {patient}")

    if not patient or not isinstance(patient, dict):
        return

    if patient.get("onboarding_email_sent"):
        return

    EventService.onboarding_email_requested(
        patient_id=patient_id,
        email=event["payload"].get("email")
    )

    try:
        send_onboarding_email(patient_id)

        EventService.onboarding_email_sent(
            patient_id=patient_id
        )

    except Exception as e:

        EventService.onboarding_email_failed(
            patient_id=patient_id,
            reason=str(e)
        )

        raise