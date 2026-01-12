from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.modules.auth.schemas import UserMe
from app.modules.auth.service import ensure_profile_exists


# ----- Auth Router -----
router = APIRouter(prefix="/auth", tags=["Auth"])


# ----- Get Current User Endpoint -----
@router.get("/me", response_model=UserMe)
def me(current_user=Depends(get_current_user)):
    ensure_profile_exists(current_user)
    return current_user