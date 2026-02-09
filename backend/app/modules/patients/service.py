from app.core.supabase_client import supabase
from app.shared.utils.timeline_event_trans_helper import transform_record_to_event
from uuid import UUID
from typing import List, Dict, Any

# ----- Get Patient Summary -----
def get_patient_summary(patient_id: str) -> Dict[str, Any]:
    """
    Generate a summary of the patient's health data including 
    vitals, conditions, and medications.  

    input: patient_id (str) - unique identifier for the patient
    return: dict - summary of patient's health data
    """
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
    condition_set = set()

    for c in conditions:
        cd = c["clinical_data"]
        clinical_status = cd.get("clinicalStatus")

        if isinstance(clinical_status, dict):
            status = (
                clinical_status
                .get("coding", [{}])[0]
                .get("code")
            )
        elif isinstance(clinical_status, str):
            status = clinical_status
        else:
            status = None

        if status == "active":
            name = cd.get("code", {}).get("text")
            if name:
                condition_set.add(name)

    condition_list = list(condition_set)


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


# ----- Transform Record to Timeline Event -----
def build_patient_timeline(patient_id: UUID):
    """
    Build a chronological timeline of a patient's medical events.
    
    input: patient_id (UUID) - unique identifier for the patient
    return: dict - timeline of medical events
    """
    response = (
        supabase
        .table("medical_records")
        .select("*")
        .eq("patient_id", str(patient_id))
        .order("created_at", desc=True)
        .execute()
    )

    records = response.data or []

    events = [
        transform_record_to_event(record)
        for record in records
        if transform_record_to_event(record) is not None
    ]

    events.sort(key=lambda e: e["date"], reverse=True)

    return {
        "patient_id": str(patient_id),
        "events": events
    }


# ----- Build Condition Resource -----
def build_condition_resource(payload: dict):
    """
    Build a FHIR Condition resource from a payload.
    Normalizes clinicalStatus and maps code.
    
    input: payload (dict) - condition data
    return: dict - FHIR Condition resource
    """
    return {
        "resourceType": "Condition",
        "clinicalStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                    "code": payload.get("status", "active"),
                    "display": payload.get("status", "active").title()
                }
            ]
        },
        "code": payload["code"],
        "onsetDateTime": payload.get("onsetDateTime")
    }


# ---- Assign Clinician to Patient ----
def assign_clinician_to_patient(
    clinician_id: str,
    patient_id: str,
    role: str,
    assigned_by: str
):
    return (
        supabase
        .table("clinicians_patients")
        .upsert({
            "clinician_id": clinician_id,
            "patient_id": patient_id,
            "role": role,
            "active": True,
            "assigned_by": assigned_by
        })
        .execute()
    ).data[0]
