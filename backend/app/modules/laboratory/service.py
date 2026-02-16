from app.modules.patient.service import require_patient_access

# ----- Build Lab Detail Response -----
def build_lab_detail(lab_id: str, current_user: dict):

    lab = fetch_lab_record(lab_id)

    require_patient_access(lab["patient_id"], current_user)

    return {
        "id": lab["id"],
        "testName": lab["test_name"],
        "status": lab["status"],
        "metadata": {
            "performedDate": lab["performed_date"],
            "orderingProvider": lab["ordering_provider"],
            "performingFacility": lab["facility_name"]
        },
        "results": lab["results"],
        "attachments": lab.get("attachments", [])
    }
