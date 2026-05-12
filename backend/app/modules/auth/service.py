import email
from fastapi import HTTPException
from app.core.supabase_client import supabase
from app.core.supabase_admin import supabase_admin



# ----- Siugnup Service [email & password] -----
def signup_user(email: str, password: str):

    res = supabase.auth.sign_up({
        "email": email,
        "password": password
    })

    # Email confirmation required
    if not res.session:
        return {
            "status": "pending_verification",
            "message": "Check your email to confirm account"
        }

    # User is immediately available
    user = res.user

    if not user:
        raise Exception("Signup failed")

    try:
        # Create patient profile
        supabase.table("profiles").insert({
            "id": user.id,
            "type": "patient"
        }).execute()

        # Get patient role
        role_resp = (
            supabase
            .table("roles")
            .select("id")
            .eq("name", "patient")
            .eq("role_type", "system")
            .single()
            .execute()
        )

        # Assign role
        supabase.table("user_roles").insert({
            "user_id": user.id,
            "role_id": role_resp.data["id"],
            "organization_id": None
        }).execute()

    except Exception as e:
        # Only rollback if session exists (real user created)
        supabase_admin.auth.admin.delete_user(user.id)
        raise Exception(f"Signup failed: {str(e)}")

    return {
        "status": "success",
        "user_id": user.id
    }


# ----- Ensure User Profile Exists -----
def ensure_profile_exists(user_id: str, user_email: str):
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
            "email": user_email
        }).execute()

    # ---- Check if role already assigned ----
    role_check = (
        supabase
        .table("user_roles")
        .select("id")
        .eq("user_id", user_id)
        .is_("organization_id", None)
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
    
    # check Id and role of user
    print("User ID:", user_id)
    print("Assigning role:", role_resp.data["id"])

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
        raise Exception(401, "Invalid credentials")
    
    user_id = response.user.id

    # Ensure onboarding is completed
    ensure_profile_exists(user_id, user_email=email)

    return {
        "access_token": response.session.access_token,
        "user": {
            "id": user_id,
            "email": response.user.email
        },
    }
