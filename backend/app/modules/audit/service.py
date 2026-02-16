from app.core.supabase_client import supabase


# ----- Audit Logging Service -----
def log_action(user_id, action, resource, resource_id, metadata=None):
    supabase.table("audit_logs").insert({
        "user_id": user_id,
        "action": action,
        "resource": resource,
        "resource_id": resource_id,
        "metadata": metadata or {}
    }).execute()
