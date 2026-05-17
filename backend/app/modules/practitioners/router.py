from fastapi import APIRouter, Depends
from app.modules.practitioners.schemas import (
    PractitionerCreate,
    PractitionerUpdate,
    PractitionerPhotoUpdate
)
from app.modules.practitioners.service import (
    create_practitioner,
    get_practitioner_by_id,
    update_practitioner,
    update_practitioner_photo
)
from app.core.security import get_current_user

router = APIRouter()


# ----- Onboard/Create Practitioner -----
@router.post("/")
def onboard_practitioner(
    payload: PractitionerCreate,
    user=Depends(get_current_user)
):
    return create_practitioner(
        user["id"],
        payload
    )


# ----- Get Practitioner -----
@router.get("/me")
def get_my_practitioner_profile(
    user=Depends(get_current_user)
):

    return get_practitioner_by_id(
        user["id"]
    )


# ----- Update Practitioner Profile -----
@router.patch("/me")
def update_my_practitioner_profile(
    payload: PractitionerUpdate,
    user=Depends(get_current_user)
):

    return update_practitioner(
        user["id"],
        payload
    )


# ----- Practitioner Upload Profile Image -----
@router.patch("/me/photo")
def update_my_practitioner_photo(
    payload: PractitionerPhotoUpdate,
    user=Depends(get_current_user)
):

    return update_practitioner_photo(
        user["id"],
        payload
    )