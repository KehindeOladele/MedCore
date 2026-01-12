from app.core.supabase_client import supabase


# ----- Ensure User Profile Exists -----
def ensure_profile_exists(user: dict):
    """
    Ensure a profiles row exists for authenticated users. Sync Supabase Auth → DB

    input: user (dict) from get_current_user
    Returns: None
    """
    user_id = user["id"]

    result = (
        supabase
        .table("profiles")
        .select("id")
        .eq("id", user_id)
        .execute()
    )

    if result.data:
        return

    # ----- Create New Profile -----
    supabase.table("profiles").insert({
        "id": user_id,
        "role": user["role"],
    }).execute()
