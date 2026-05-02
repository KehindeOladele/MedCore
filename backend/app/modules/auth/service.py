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
    
    try:
        # Create patient profile
        supabase.table("profiles").insert({
            "id": user.id,
            "type": "patient"
        }).execute()

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
            raise Exception("Role not found")

        # ---- Assign role ----
        supabase.table("user_roles").insert({
            "user_id": user.id,
            "role_id": role_resp.data["id"],
            "organization_id": None
        }).execute()

    except Exception as e:
        # Rollback user creation on failure
        supabase.auth.admin.delete_user(user.id)
        raise Exception(f"Signup failed: {str(e)}")

    return {
        "message": "Signup successful",
        "user_id": user.id
    }


# ----- Ensure User Profile Exists -----
def ensure_profile_exists(user):
    """
    Ensure a profiles row exists for authenticated users. Sync Supabase Auth → DB

    input: user (dict) from get_current_user
    Returns: None
    """
    user_id = user["id"] if isinstance(user, dict) else user.id
    user_email= user["email"] if isinstance(user, dict) else user.email

    response = (
        supabase
        .table("profiles")
        .select("id")
        .eq("id", user_id)
        .execute()
    )

    if response.data:
        return

    # ----- Create New Profile -----
    supabase.table("profiles").insert({
        "id": user_id,
        "email": user_email,
        "role": "patient",
    }).execute()


# ---- Login Service [email & password] -----
def login_user(email: str, password: str):

    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    if not response.user:
        raise Exception("Invalid credentials")

    user = response.user
    session = response.session

    # ---- Fetch roles from your DB ----
    role_resp = (
        supabase
        .table("user_roles")
        .select("role_id, roles(name, role_type), organization_id")
        .eq("user_id", user.id)
        .execute()
    )

    roles = role_resp.data or []

    # Flatten roles
    user_roles = [
        {
            "role": r["roles"]["name"],
            "role_type": r["roles"]["role_type"],
            "organization_id": r["organization_id"]
        }
        for r in roles
    ]

    return {
        "access_token": session.access_token,
        "refresh_token": session.refresh_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "roles": user_roles
        }
    }