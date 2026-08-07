from app.core.supabase_admin import supabase_admin

def delete_auth_user(user_id: str):
    try:
        supabase_admin.auth.admin.delete_user(user_id)
    except Exception as e:
        raise Exception(f"Failed to delete user: {str(e)}")