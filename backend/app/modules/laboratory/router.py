from fastapi import APIRouter, Depends
from app.modules.patient.service import get_current_user
from .service import build_lab_detail


router = APIRouter()


# -----Get Lab Result Endpoint -----
@router.get("/api/v1/lab-results/{lab_id}")
def get_lab_result(
    lab_id: str,
    current_user=Depends(get_current_user)
):
    return build_lab_detail(lab_id, current_user)
