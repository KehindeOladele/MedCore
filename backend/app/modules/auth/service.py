import email

from app.core.supabase_client import supabase


# ----- Siugnup Service [email & password] -----
def signup_user(email: str, password: str):
    # ---- Create user in Supabase Auth ----
    res = supabase.auth.sign_up({
        "email": email,
        "password": password
    })

    user = res.user

    if not user:
        raise Exception("Signup failed")
    
    # ---- Email Confirmation -----
    if not res.session:
        return {
            "message": "Check your email to confirm account"
        }

    return {
        "message": "Signup successful",
        "user_id": user.id
    }


# ----- Ensure User Profile Exists -----
def ensure_profile_exists(user_id: str):
    """
    Ensure a profiles row exists for authenticated users. Sync Supabase Auth → DB

    input: user (dict) from get_current_user
    Returns: None
    """
# ---- Check if profile exists ----
    profile = (
        supabase
        .table("profiles")
        .select("id")
        .eq("id", user_id)
        .execute()
    )

    if not profile.data:
        supabase.table("profiles").insert({
            "id": user_id,
            "type": "patient"
        }).execute()

    # ---- Check if role already assigned ----
    role_check = (
        supabase
        .table("user_roles")
        .select("id")
        .eq("user_id", user_id)
        .execute()
    )

    if role_check.data:
        return  # already onboarded (idempotent)

    # ---- Get patient role ----
    role_resp = (
        supabase
        .table("roles")
        .select("id")
        .eq("name", "patient")
        .eq("role_type", "system")
        .single()
        .execute()
    )

    if not role_resp.data:
        raise Exception("Patient role not configured")

    # ---- Assign role ----
    supabase.table("user_roles").insert({
        "user_id": user_id,
        "role_id": role_resp.data["id"],
        "organization_id": None
    }).execute()


# ---- Login Service [email & password] -----
def login_user(email: str, password: str):

    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    if not response.user:
        raise Exception("Invalid credentials")
    
    user_id = response.user.id

    # Ensure onboarding is completed
    ensure_profile_exists(user_id)

    return {
        "access_token": response.session.access_token,
        "user": response.user,
    }