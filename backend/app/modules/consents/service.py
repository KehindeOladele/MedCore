from app.core.supabase_admin import supabase_admin
from fastapi import HTTPException
from datetime import datetime, timezone


# ----- Grant Consent Service for Practitioners -----
def grant_consent(
    patient_id: str,
    payload
):

    response = (
        supabase_admin
        .table("consent_records")
        .insert({
            "patient_id": patient_id,
            "organization_id": payload.organization_id,
            "practitioner_id": payload.practitioner_id,
            "consent_type": payload.consent_type,
            "access_level": payload.access_level,
            "purpose_of_use": payload.purpose_of_use,
            "legal_basis": payload.legal_basis,
            "emergency_access": payload.emergency_access,
            "effective_from": (
                payload.effective_from.isoformat()
                if payload.effective_from else None
            ),

            "expires_at": (
                payload.expires_at.isoformat()
                if payload.expires_at else None
            ),

            "metadata": payload.metadata,
            "status": "active"
        })
        .execute()
    )

    return response.data[0]


# ----- Revoke Consent Service -----
def revoke_consent(
    patient_id: str,
    payload
):

    existing = (
        supabase_admin
        .table("consent_records")
        .select("*")
        .eq("id", payload.consent_id)
        .eq("patient_id", patient_id)
        .limit(1)
        .execute()
    )

    if not existing.data:
        raise HTTPException(
            status_code=404,
            detail="Consent not found"
        )

    response = (
        supabase_admin
        .table("consent_records")
        .update({
            "status": "revoked",
            "revoked_reason": payload.revoked_reason,
            "revoked_at": (
                datetime.now(timezone.utc)
                .isoformat()
            )
        })
        .eq("id", payload.consent_id)
        .execute()
    )

    return response.data[0]


# ---- Get List of Existing Consent Service ----
def get_patient_consents(
    patient_id: str
):

    response = (
        supabase_admin
        .table("consent_records")
        .select("""
            *,
            organizations (
                id,
                name
            ),
            practitioners (
                id,
                first_name,
                last_name,
                photo
            )
        """)
        .eq("patient_id", patient_id)
        .order("created_at", desc=True)
        .execute()
    )

    return response.data