from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import get_current_user
from app.modules.auth.schemas import (
    UserMe, 
    SignupRequest,
)
from app.modules.auth.service import (
    ensure_profile_exists, 
    signup_user,
    login_user,
)


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
    

# --------------------------
# Login Endpoint 
# --------------------------
@router.post("/login")
def login(
    background_tasks: BackgroundTasks,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    OAuth2 Password Flow login.

    Expects:
        Content-Type: application/x-www-form-urlencoded

        username=<email>
        password=<password>
    """

    response = login_user(
        email=form_data.username,
        password=form_data.password
    )

    return response
