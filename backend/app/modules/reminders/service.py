from app.core.supabase_client import supabase
from datetime import datetime


# ----- Reminder Service -----
def get_upcoming_reminders(patient_id: str):
    now = datetime.utcnow().isoformat()

    response = (
        supabase
        .table("reminders")
        .select("*")
        .eq("patient_id", patient_id)
        .gte("scheduled_at", now)
        .execute()
    )

    return response.data or []
