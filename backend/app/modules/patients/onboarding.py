from datetime import datetime

from app.core.supabase_admin import supabase_admin

from app.shared.services.email_service import send_email
from app.shared.services.template_service import render_template


# ----- Send Onboarding Patient Email -----
def send_patient_welcome_email(patient_id: str):

    patient = (
        supabase_admin
        .table("patients")
        .select("*")
        .eq("id", patient_id)
        .single()
        .execute()
    )

    patient_data = patient.data

    if not patient_data:
        return

    # Prevent duplicate onboarding
    if patient_data.get("onboarding_completed"):
        return

    html = render_template(
        "emails/welcome_patient.html",
        {
            "first_name": patient_data.get("first_name"),
            "medical_id": patient_data.get("medical_id")
        }
    )

    send_email(
        to_email=patient_data["email"],
        subject="Welcome to MedCore",
        html=html
    )

    # Mark onboarding complete
    supabase_admin.table("patients").update({
        "onboarding_completed": True,
        "onboarding_completed_at": datetime.utcnow().isoformat()
    }).eq("id", patient_id).execute()