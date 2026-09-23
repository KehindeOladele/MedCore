from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.modules.consents.schemas import (
    ConsentGrant,
    ConsentRevoke
)
from app.modules.consents.service import (
    grant_consent,
    revoke_consent,
    get_patient_consents
)


router = APIRouter(
    prefix="/consents",
    tags=["Consents"]
)


# ----- Grant Consent endpoint -----
@router.post("/grant")
def create_consent(
    payload: ConsentGrant,
    user=Depends(get_current_user)
):

    return grant_consent(
        user["id"],
        payload
    )


#  ----- Revoke Consent endpoint -----
@router.post("/revoke")
def revoke_patient_consent(
    payload: ConsentRevoke,
    user=Depends(get_current_user)
):

    return revoke_consent(
        user["id"],
        payload
    )


# ----- Get List Patinets Consents -----
@router.get("/me")
def my_consents(
    user=Depends(get_current_user)
):

    return get_patient_consents(
        user["id"]
    )