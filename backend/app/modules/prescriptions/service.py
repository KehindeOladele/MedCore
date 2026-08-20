from app.core.supabase_client import supabase


#  ----- Service functions for prescriptions -----
def get_active_prescriptions(patient_id: str):
    response = (
        supabase
        .table("prescriptions")
        .select("*")
        .eq("patient_id", patient_id)
        .eq("status", "active")
        .execute()
    )

    return response.data or []
