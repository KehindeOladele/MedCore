from app.core.supabase_admin import supabase_admin
from app.core.security import get_current_user
from fastapi import Depends, HTTPException


# ----- Manual Authorization for Patient Access ----- 
def require_patient_access_manual(
    patient_id: str,
    user_id: str
):
    res = (
        supabase_admin
        .table("patient_access")
        .select("id")
        .eq("patient_id", patient_id)
        .eq("user_id", user_id)
        .single()
        .execute()
    )

    if not res.data:
        raise HTTPException(403, "No access to this patient")

    return True