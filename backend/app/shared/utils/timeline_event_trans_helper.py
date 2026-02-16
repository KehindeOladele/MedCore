# ----- Parse Condition Event -----
def parse_condition_event(record) -> dict:
    """
    function parse_condition_event, 
    enhance timeline events for conditions 
    (status, onset date, SNOMED code).
    
    input: record (dict) - medical record
    return: dict - enhanced timeline event
    """
    data = record["clinical_data"]

    # ---- Code (SNOMED) ----
    code_block = data.get("code", {})
    coding = code_block.get("coding", [{}])[0] if isinstance(code_block, dict) else {}

    # ---- Clinical Status (FHIR-safe) ----
    clinical_status = data.get("clinicalStatus")

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

    return {
        "id": record.get("id"),
        "type": "condition",
        "date": data.get("onsetDateTime") or record["created_at"],
        "end_date": data.get("abatementDateTime"),
        "title": (
            coding.get("display")
            or code_block.get("text")
            or "Condition"
        ),
        "status": status,
        "code": {
            "system": "SNOMED",
            "code": coding.get("code"),
            "display": coding.get("display")
        }
    }


# ----- Parse Observation Event -----
def parse_observation_event(record: dict) -> dict:
    """
    Function parse_observation_event,
    enhance timeline events for observations.

    input: record (dict) - medical record
    return: dict - enhanced timeline event
    """
    data = record["clinical_data"]

    return {
        "type": "observation",
        "date": record["created_at"],
        "title": data.get("code", {}).get("text"),
        "value": data.get("valueQuantity", {}).get("value"),
        "unit": data.get("valueQuantity", {}).get("unit")
    }


# ------ Parse Medication Event -----
def parse_medication_event(record: dict) -> dict:
    """
    Function parse_medication_event,
    enhance timeline events for medications.

    input: record (dict) - medical record
    return: dict - enhanced timeline event
    """
    data = record["clinical_data"]

    coding = (
        data.get("medicationCodeableConcept", {})
            .get("coding", [{}])[0]
    )

    return {
        "type": "medication",
        "date": data.get("authoredOn") or record["created_at"],
        "title": coding.get("display"),
        "code": {
            "system": "RxNorm",
            "code": coding.get("code"),
            "display": coding.get("display")
        }
    }


# ----- Transform Record to Event -----
def transform_record_to_event(record: dict) -> dict | None:
    """
    Transform a medical record into a timeline event based on its type.

    input: record (dict) - medical record
    return: dict | None - timeline event or None if type is unrecognized
    """ 
    record_type = record.get("record_type")

    if record_type == "condition":
        return parse_condition_event(record)

    if record_type == "observation":
        return parse_observation_event(record)

    if record_type == "medication":
        return parse_medication_event(record)

    return None
