from app.core.supabase_client import supabase
from uuid import UUID
from typing import List, Dict, Any


def get_patient_summary(patient_id: str) -> Dict[str, Any]:
    # ---- Fetch patient ----
    patient_resp = (
        supabase
        .table("patients")
        .select("*")
        .eq("id", patient_id)
        .single()
        .execute()
    )

    if not patient_resp.data:
        raise ValueError("Patient not found")

    patient = patient_resp.data

    # ---- Fetch all medical records ----
    records_resp = (
        supabase
        .table("medical_records")
        .select("*")
        .eq("patient_id", patient_id)
        .order("created_at", desc=True)
        .execute()
    )

    records = records_resp.data or []

    observations = []
    conditions = []
    medications = []

    for r in records:
        if r["record_type"] == "observation":
            observations.append(r)
        elif r["record_type"] == "condition":
            conditions.append(r)
        elif r["record_type"] == "medication":
            medications.append(r)

    # ---- Extract vitals (latest only) ----
    vitals = {}
    if observations:
        latest_obs = observations[0]["clinical_data"]
        vitals = {
            "name": latest_obs.get("code", {}).get("text"),
            "value": latest_obs.get("valueQuantity", {}).get("value"),
            "unit": latest_obs.get("valueQuantity", {}).get("unit"),
            "recorded_at": observations[0]["created_at"]
        }

    # ---- Extract conditions ----
    condition_list = []
    for c in conditions:
        cd = c["clinical_data"]
        condition_list.append(
            cd.get("code", {}).get("text")
        )

    # ---- Extract medications ----
    medication_list = []
    for m in medications:
        cd = m["clinical_data"]
        medication_list.append({
            "name": cd["medicationCodeableConcept"]["coding"][0]["display"],
            "authored_on": cd.get("authoredOn")
        })

    # ---- Build summary ----
    summary = {
        "patient": {
            "id": patient["id"],
            "first_name": patient.get("first_name"),
            "last_name": patient.get("last_name"),
            "gender": patient.get("gender"),
            "date_of_birth": patient.get("date_of_birth")
        },
        "vitals": vitals,
        "conditions": condition_list,
        "medications": medication_list,
        "last_updated": records[0]["created_at"] if records else None
    }

    return summary


# ----- Get or Create Patient -----
def get_or_create_patient(user_id: str):
    response = (
        supabase
        .table("patients")
        .select("*")
        .eq("id", user_id)
        .execute()
    )

    if response.data:
        return response.data[0]

    insert = (
        supabase
        .table("patients")
        .insert({
            "id": user_id,
            "fhir_metadata": {
                "resourceType": "Patient"
            }
        })
        .execute()
    )

    if not insert.data:
        raise Exception("Failed to create patient record")

    return insert.data[0]


# ----- Get Patient with Records -----
def get_patient_with_records(patient_id: str):
    patient = (
        supabase
        .table("patients")
        .select("*")
        .eq("id", patient_id)
        .single()
        .execute()
    ).data

    records = (
        supabase
        .table("medical_records")
        .select("clinical_data")
        .eq("patient_id", patient_id)
        .execute()
    ).data

    return patient, records

