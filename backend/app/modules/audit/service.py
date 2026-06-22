from app.core.supabase_admin import supabase_admin


# ----- Audit Logging Service -----
def log_audit_event(
    *,
    actor_id: str | None,
    actor_type: str | None,
    action: str,
    resource_type: str,
    resource_id: str,
    metadata: dict | None = None
):
    (
        supabase_admin
        .table("audit_logs")
        .insert({
            "actor_id": actor_id,
            "actor_type": actor_type,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "metadata": metadata or {}
        })
        .execute()
    )