from app.core.supabase_client import supabase


# ----- Siugnup Service [email & password] -----
def sign_up(email: str, password: str):
    
    # ----- Create user in Supabase Auth -----
    response = supabase.auth.sign_up({
        "email": email,
        "password": password
    })
    
    # ----- Return Response -----
    user = response.user
    if not user:
        return {"error": response.get("error")}

    # ----- Return user info -----
    return user


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
