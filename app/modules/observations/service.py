from fastapi import HTTPException
from app.core.supabase_admin import supabase_admin


# ----- Create Observation Service -----
def create_observation(
    payload,
    created_by: str
):
    
    if not payload.patient_id:
        raise HTTPException(400, "patient_id required")

    response = (
        supabase_admin
        .table("observations")
        .insert({
            "patient_id": payload.patient_id,
            "encounter_id": payload.encounter_id,
            "organization_id": payload.organization_id,
            "practitioner_id": payload.practitioner_id,
            "category": payload.category,
            "code": payload.code,
            "display": payload.display,
            "value": payload.value,
            "unit": payload.unit,
            "interpretation": payload.interpretation,
            "status": payload.status,
            "effective_at": (
                payload.effective_at.isoformat()
                if payload.effective_at else None
            ),
            "issued_at": (
                payload.issued_at.isoformat()
                if payload.issued_at else None
            ),
            "notes": payload.notes,
            "metadata": payload.metadata,
            "created_by": created_by
        })
        .execute()
    )

    return response.data[0]


# ----- Get Patient Observations Service -----
def get_patient_observations(
    patient_id: str
):

    response = (
        supabase_admin
        .table("observations")
        .select("""
            *,
            practitioners (
                id,
                first_name,
                last_name
            )
        """)
        .eq("patient_id", patient_id)
        .order(
            "effective_at",
            desc=True
        )
        .execute()
    )

    return response.data


# ---- Get Encounter Observation Service -----
def get_encounter_observations(
    encounter_id: str
):

    response = (
        supabase_admin
        .table("observations")
        .select("*")
        .eq("encounter_id", encounter_id)
        .order(
            "effective_at",
            desc=True
        )
        .execute()
    )

    return response.data


# ---- Update Observatiom Service -----
def update_observation(
    observation_id: str,
    payload
):

    update_data = payload.model_dump(
        exclude_unset=True
    )

    response = (
        supabase_admin
        .table("observations")
        .update(update_data)
        .eq("id", observation_id)
        .execute()
    )

    return response.data[0]


# ----- Validate Encounter -----
def validate_encounter(encounter_id, patient_id):

    res = (
        supabase_admin
        .table("encounters")
        .select("patient_id")
        .eq("id", encounter_id)
        .single()
        .execute()
    )

    if not res.data:
        raise HTTPException(404, "Encounter not found")

    if res.data["patient_id"] != patient_id:
        raise HTTPException(400, "Encounter does not belong to patient")