from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.core.audit.query import get_resource_audit_log


router = APIRouter(
    prefix="/admin/audit",
    tags=["Audit"]
)


# ------------------
# Get Audit Endpoint
# ------------------
@router.get("/{resource_type}/{resource_id}")
def get_audit(
    resource_type: str,
    resource_id: str,
    user=Depends(get_current_user)
):
    return get_resource_audit_log(
        resource_type,
        resource_id
    )