from fastapi import APIRouter, Depends, HTTPException 
from app.core.security import get_current_user
from app.modules.auth.schemas import UserMe, SignupRequest, SignupResponse
from app.modules.auth.service import ensure_profile_exists, sign_up
# from app.core.supabase_client import supabase


# ----- Auth Router -----
router = APIRouter(prefix="/auth", tags=["Auth"])


# ----- Get Current User Endpoint -----
@router.get("/me", response_model=UserMe)
def me(current_user=Depends(get_current_user)):
    ensure_profile_exists(current_user)
    return current_user


# ----- Signup Endpoint -----
@router.post("/signup", response_model=SignupResponse)
def signup(req: SignupRequest):
    try: 
        # ----- Create user in Supabase Auth -----
        user= sign_up(req.email, req.password)

        # ----- Auto-create profile -----
        ensure_profile_exists(user)

        # ----- Return user info -----
        return {
            "id": user.id, 
            "email": user.email, 
            "role": "patient"
            }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))