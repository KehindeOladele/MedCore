from __future__ import annotations
from datetime import datetime, timezone

from typing import Any
from uuid import UUID

from app.core.supabase_client import supabase
from .schemas import (
    HealthcareServiceCreate,
    HealthcareServiceUpdate,
)
from .constants import TABLE


# ------------------------------------------------------------
# CREATE HEALTHCARE SERVICE 
# ------------------------------------------------------------
def create_healthcare_service(
    organization_id: UUID,
    payload: HealthcareServiceCreate,
    *,
    created_by: UUID | None = None,
) -> dict[str, Any]:
    """
    Insert a new healthcare service.
    """

    data = payload.model_dump(exclude_none=True)

    data["organization_id"] = str(organization_id)
    data["created_by"] = str(created_by) if created_by else None
    data["updated_by"] = str(created_by) if created_by else None

    response = (
        supabase.table(TABLE)
        .insert(data)
        .execute()
    )

    return response.data[0]


# ------------------------------------------------------------
# GET HEALTHCARE SERVICE 
# ------------------------------------------------------------
def get_healthcare_service(
    organization_id: UUID,
    healthcare_service_id: UUID,
) -> dict[str, Any] | None:
    """
    Retrieve a healthcare service by ID.
    """

    response = (
        supabase.table(TABLE)
        .select("*")
        .eq("organization_id", str(organization_id))
        .eq("id", str(healthcare_service_id))
        .is_("deleted_at", "null")
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


# ------------------------------------------------------------
# LIST HEALTHCARE SERVICE 
# ------------------------------------------------------------
def list_healthcare_services(
    organization_id: UUID,
    *,
    active_only: bool = False,
) -> list[dict[str,Any]]:
    """
    List healthcare services for an organization.
    """

    query = (
        supabase.table(TABLE)
        .select("*")
        .eq("organization_id", str(organization_id))
        .is_("deleted_at", "null")
        .order("display_order")
        .order("name")
    )

    if active_only:
        query = query.eq("active", True)

    response = query.execute()

    return response.data


# ------------------------------------------------------------
# UPDATE HEALTHCARE SERVICE 
# ------------------------------------------------------------
def update_healthcare_service(
    organization_id: UUID,
    healthcare_service_id: UUID,
    payload: HealthcareServiceUpdate,
    *,
    updated_by: UUID | None = None,
) -> dict[str, Any]:
    """
    Update a healthcare service.
    """

    updates = payload.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    if updated_by:
        updates["updated_by"] = str(updated_by)

    response = (
        supabase.table(TABLE)
        .update(updates)
        .eq("organization_id", str(organization_id))
        .eq("id", str(healthcare_service_id))
        .execute()
    )

    return response.data[0]


# ------------------------------------------------------------
# SOFT DELETE HEALTHCARE SERVICE 
# ------------------------------------------------------------
def delete_healthcare_service(
    organization_id: UUID,
    healthcare_service_id: UUID,
    *,
    deleted_by: UUID | None = None,
) -> dict:
    """
    Soft delete a healthcare service.
    """

    updates = {
        "deleted_at": datetime.now(timezone.utc).isoformat(),
        "active": False,
    }

    if deleted_by:
        updates["updated_by"] = str(deleted_by)

    response = (
        supabase.table(TABLE)
        .update(updates)
        .eq("organization_id", str(organization_id))
        .eq("id", str(healthcare_service_id))
        .execute()
    )

    return response.data[0]


# ------------------------------------------------------------
# DUPLICATE HEALTHCARE SERVICE CHECK 
# ------------------------------------------------------------
def get_healthcare_service_by_name(
    organization_id: UUID,
    name: str,
) -> dict | None:
    """
    Retrieve a healthcare service by name.
    """

    response = (
        supabase.table(TABLE)
        .select("*")
        .eq("organization_id", str(organization_id))
        .eq("name", name)
        .is_("deleted_at", "null")
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


# ------------------------------------------------------------
# LIST HEALTHCARE SERVICE DEPARTMENT
# ------------------------------------------------------------
def list_department_healthcare_services(
    organization_id: UUID,
    department_id: UUID,
) -> list[dict]:
    """
    List all healthcare services belonging to a department.
    """

    response = (
        supabase.table(TABLE)
        .select("*")
        .eq("organization_id", str(organization_id))
        .eq("department_id", str(department_id))
        .is_("deleted_at", "null")
        .order("display_order")
        .order("name")
        .execute()
    )

    return response.data