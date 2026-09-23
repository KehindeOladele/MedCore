from app.core.supabase_admin import supabase_admin


# --------------
# Query Resource
# -------------- 
def get_resource_audit_log(
    resource_type: str,
    resource_id: str
):
    return (
        supabase_admin
        .table("audit_logs")
        .select("*")
        .eq("resource_type", resource_type)
        .eq("resource_id", resource_id)
        .order("created_at", desc=True)
        .execute()
        .data
    )