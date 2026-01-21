def transform_record_to_event(record: dict):
    clinical = record["clinical_data"]
    record_type = record["record_type"]

    if record_type == "observation":
        title = clinical.get("code", {}).get("text", "Observation")
        value = clinical.get("valueQuantity", {})
        description = f"{value.get('value')} {value.get('unit')}"

    elif record_type == "condition":
        title = clinical.get("code", {}).get("text", "Condition")
        description = clinical.get("clinicalStatus", {}).get("text", "")

    elif record_type == "medication":
        title = clinical["medicationCodeableConcept"]["coding"][0]["display"]
        description = clinical.get("status", "active")

    else:
        title = record_type
        description = ""

    return {
        "id": record["id"],
        "type": record_type,
        "title": title,
        "description": description,
        "timestamp": record["created_at"],
        "source": "clinician"
    }
