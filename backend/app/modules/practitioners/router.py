from fastapi import APIRouter, Depends
from app.modules.practitioners.schemas import PractitionerCreate
from app.modules.practitioners.service import create_practitioner
from app.core.security import get_current_user

router = APIRouter()


@router.post("/")
def onboard_practitioner(
    payload: PractitionerCreate,
    user=Depends(get_current_user)
):
    return create_practitioner(
        user["id"],
        payload
    )