from app.core.security import require_patient_access
from app.core.supabase_client import supabase


# ----- Fetch Lab Record from Database -----
def fetch_lab_record(lab_id: str) -> dict:
    response = (
        supabase
        .table("lab_records")
        .select("*")
        .eq("id", lab_id)
        .single()
        .execute()
    )

    if not response.data:
        return None

    return response.data


# ----- Build Lab Detail Response -----
def build_lab_detail(lab_id: str, current_user: dict) -> dict:

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
