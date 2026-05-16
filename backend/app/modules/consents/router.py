from fastapi import APIRouter, Depends

from app.core.security import get_current_user

from app.modules.consents.schemas import ConsentGrant
from app.modules.consents.service import grant_consent


router = APIRouter(
    prefix="/consents",
    tags=["Consents"]
)


@router.post("/grant")
def create_consent(
    payload: ConsentGrant,
    user=Depends(get_current_user)
):

    return grant_consent(
        user["id"],
        payload
    )