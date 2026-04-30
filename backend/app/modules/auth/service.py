from app.core.supabase_client import supabase


# ----- Siugnup Service [email & password] -----
def signup_user(email: str, password: str):

    # ---- Check if user is invited (staff flow) ----
    invite_resp = (
        supabase
        .table("invitations")
        .select("*")
        .eq("email", email)
        .eq("status", "pending")
        .execute()
    )

    is_invited = bool(invite_resp.data)

    # ---- If NOT invited → treat as patient signup ----
    if not is_invited:
        # Allow only patient self-signup
        role_name = "patient"
        org_id = None
    else:
        # Staff signup via invite
        invite = invite_resp.data[0]
        role_name = invite["role_name"]
        org_id = invite["organization_id"]

    # ---- Create user in Supabase Auth ----
    res = supabase.auth.sign_up({
        "email": email,
        "password": password
    })

    user = res.user

    if not user:
        raise Exception("Signup failed")

    # ---- Assign role ----
    role_resp = (
        supabase
        .table("roles")
        .select("id")
        .eq("name", role_name)
        .execute()
    )

    if not role_resp.data:
        raise Exception("Role not found")

    role_id = role_resp.data[0]["id"]

    supabase.table("user_roles").insert({
        "user_id": user.id,
        "role_id": role_id,
        "organization_id": org_id
    }).execute()

    # ---- Mark invite accepted (if exists) ----
    if is_invited:
        supabase.table("invitations").update({
            "status": "accepted"
        }).eq("id", invite["id"]).execute()

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