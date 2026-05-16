from fastapi import HTTPException
from app.core.supabase_admin import supabase_admin


# ----- Care Team Assignment Service ----
def assign_care_team(
    practitioner_id: str,
    payload,
    assigned_by: str
):

    existing = (
        supabase_admin
        .table("patient_care_team")
        .select("id")
        .eq("patient_id", payload.patient_id)
        .eq("practitioner_id", practitioner_id)
        .eq("organization_id", payload.organization_id)
        .execute()
    )

    if existing.data:
        raise HTTPException(
            status_code=400,
            detail="Already assigned"
        )

    response = (
        supabase_admin
        .table("patient_care_team")
        .insert({
            "patient_id": payload.patient_id,
            "practitioner_id": practitioner_id,
            "organization_id": payload.organization_id,
            "role": payload.role,
            "notes": payload.notes,
            "assigned_by": assigned_by,
        })
        .execute()
    )

    return response.data[0]