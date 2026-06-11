from app.core.events.emitter import emit_event
from app.core.events.schemas import EventTypes
from app.core.events.registry import register
from app.core.events.emitter import emit_event
from app.modules.patients.onboarding import send_onboarding_email
from app.core.supabase_admin import supabase_admin
from app.core.events.service import EventService



# ----- Patient Create Hanlder ----- 
@register(EventTypes.PATIENT_CREATED)
def handle_patient_created(event):

    EventService.patient_created(
        patient_id=event["aggregate_id"],
        email=event["payload"].get("email")
    )

    handle_onboarding_email_requested(event)


# ----- Onboarding Email Request Handler -----
@register(EventTypes.ONBOARDING_EMAIL_REQUESTED)
def handle_onboarding_email_requested(event):

    patient_id = event["aggregate_id"]
    
    patient = (
        supabase_admin
        .table("patients")
        .select("onboarding_email_sent")
        .eq("id", patient_id)
        .single()
        .execute()
    ).data

    EventService.onboarding_email_requested(
        patient_id=patient_id,
        email=event["payload"].get("email")
    )

    if patient.get("onboarding_email_sent"):
        return

    EventService.onboarding_email_sent(
        patient_id=patient_id
        )