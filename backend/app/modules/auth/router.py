from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.core.security import get_current_user
from app.modules.auth.schemas import (
    UserMe, 
    SignupRequest, 
    SignupResponse,
    LoginRequest
)
from app.modules.auth.service import (
    ensure_profile_exists, 
    signup_user,
    login_user
)
from app.modules.patients.onboarding import send_onboarding_email
# from app.core.supabase_client import supabase


# ----- Auth Router -----
router = APIRouter(prefix="/auth", tags=["Auth"])


# ----- Get Current User Endpoint -----
@router.get("/me", response_model=UserMe)
def me(current_user=Depends(get_current_user)):
    ensure_profile_exists(current_user["id"], current_user["email"])
    return current_user


# ----- Signup Endpoint -----
@router.post("/signup")
def signup(req: SignupRequest): 
    # ----- Create user in Supabase Auth -----
    user= signup_user(req.email, req.password)

    # If pending verification → return early
    if user.get("status") == "pending_verification":
        return user

    # Otherwise it's success
    return user
    

# ----- Login Endpoint -----
@router.post("/login")
def login(
    payload: LoginRequest,
    background_tasks: BackgroundTasks
):

    response = login_user(
        payload.email,
        payload.password
    )

    background_tasks.add_task(
        send_onboarding_email,
        response["user"]["id"]
    )

    return response 