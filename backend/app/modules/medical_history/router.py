from fastapi import APIRouter, Depends
from .service import get_patient_history
from ..auth import get_current_user

router = APIRouter()


# ----- Endpoint to get the medical history for the current user -----
@router.get("/api/v1/medical-history")
def medical_history(current_user=Depends(get_current_user)):
    return {
        "data": get_patient_history(current_user["id"])
    }
