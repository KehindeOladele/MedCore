from datetime import datetime, timezone
from app.core.supabase_admin import supabase_admin
from app.shared.email.email_service import send_email
from app.shared.services.template_service import render_template
from app.shared.schemas.email_service import EmailService
from app.modules.patients.exceptions import EmailDeliveryError
import logging

logger = logging.getLogger(__name__)


# ----- Onboarding Patient Email Serivice -----
def send_onboarding_email(patient_id: str):

    try:
        patient = (
            supabase_admin
            .table("patients")
            .select("*")
            .eq("id", patient_id)
            .single()
            .execute()
        ).data
    except Exception:
        logger.warning(f"Patient not found: {patient_id}")
        return

    if not patient:
        return {"status": "not_found"}
    
    if patient.get("onboarding_email_sent") and patient.get("onboarding_completed"):
        return

    email = patient.get("email")

    if not email:
        return {"status": "missing_email"}

    try:

        html = render_template(
            "emails/welcome_patient.html",
            {
                "first_name": patient.get("first_name"),
                "medical_id": patient.get("medical_id")
            }
        )

        response = send_email(
            EmailService(
                to=email,
                subject="Welcome to MedCore",
                html=html
            )
        )

        if not response:
            raise EmailDeliveryError("Email send failed")
        
        now = datetime.now(timezone.utc).isoformat()

        (
            supabase_admin
            .table("patients")
            .update({
                "onboarding_email_sent": True,
                "onboarding_email_sent_at": now,
                "onboarding_retry_count": 0,
                "onboarding_last_error": None
            })
            .eq("id", patient_id)
            .execute()
        )

    except Exception as e:
        logger.exception(
            f"Failed onboarding email for patient {patient_id}: {str(e)}"
        )

        (
            supabase_admin
            .table("patients")
            .update({
                "onboarding_last_error": str(e),
                "onboarding_failure_reason": "email_delivery_failed",
                "onboarding_retry_count": patient.get("onboarding_retry_count", 0) + 1,
                "onboarding_status": "failed"
            })
            .eq("id", patient_id)
            .execute()
        )

        raise