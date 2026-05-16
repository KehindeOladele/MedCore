from app.core.supabase_admin import supabase_admin


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
            "status": "active",
            "expires_at": payload.expires_at,
        })
        .execute()
    )

    return response.data[0]