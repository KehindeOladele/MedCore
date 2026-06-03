from datetime import datetime, timezone

from app.core.supabase_admin import supabase_admin

from app.shared.email.email_service import send_email
from app.shared.services.template_service import render_template
from app.shared.schemas.email_service import EmailService
import logging

logger = logging.getLogger(__name__)


# ----- Send Onboarding Patient Email -----
def send_patient_welcome_email(patient_id: str):

    patient = (
        supabase_admin
        .table("patients")
        .select("*")
        .eq("id", patient_id)
        .limit(1)
        .execute()
    )

    patient_data = patient.data

    if not patient_data:
        return

    if patient_data.get("onboarding_completed"):
        return

    email = patient_data.get("email")

    if not email:
        return

    html = render_template(
        "emails/welcome_patient.html",
        {
            "first_name": patient_data.get("first_name"),
            "medical_id": patient_data.get("medical_id")
        }
    )

    email_service = EmailService(
        to=email,
        subject="Welcome to MedCore",
        html=html
    )

    try:
        send_email(email_service)

        supabase_admin.table("patients").update({
            "onboarding_completed": True,
            "onboarding_completed_at": datetime.now(timezone.utc).isoformat()
        }).eq("id", patient_id).execute()

        if not patient.data:
            logger.warning(f"Patient not found: {patient_id}")
            return

    except Exception:
        logger.exception(f"Failed onboarding email for patient {patient_id}")
        raise