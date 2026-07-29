from typing import Any
from uuid import UUID

from app.core.supabase_client import supabase


TABLE_NAME = "departments"


# ---------------------------------------------------------
# Create
# ---------------------------------------------------------

def create_department(data: dict[str, Any]) -> dict:
    """
    Insert a new department.
    """

    response = (
        supabase
        .table(TABLE_NAME)
        .insert(data)
        .execute()
    )

    return response.data[0]


# ---------------------------------------------------------
# Get by ID
# ---------------------------------------------------------

def get_department(
    organization_id: UUID,
    department_id: UUID,
) -> dict | None:
    """
    Retrieve a department by ID.
    """

    response = (
        supabase
        .table(TABLE_NAME)
        .select("*")
        .eq("organization_id", str(organization_id))
        .eq("id", str(department_id))
        .is_("deleted_at", "null")
        .maybe_single()
        .execute()
    )

    return response.data


# ---------------------------------------------------------
# List Departments
# ---------------------------------------------------------

def list_departments(
    organization_id: UUID,
) -> list[dict]:
    """
    Retrieve all active departments for an organization.
    """

    response = (
        supabase
        .table(TABLE_NAME)
        .select("*")
        .eq("organization_id", str(organization_id))
        .is_("deleted_at", "null")
        .order("name")
        .execute()
    )

    return response.data


# ---------------------------------------------------------
# Department Exists
# ---------------------------------------------------------

def department_exists(
    organization_id: UUID,
    name: str,
) -> bool:
    """
    Check whether a department already exists.
    """

    response = (
        supabase
        .table(TABLE_NAME)
        .select("id")
        .eq("organization_id", str(organization_id))
        .eq("name", name)
        .is_("deleted_at", "null")
        .maybe_single()
        .execute()
    )

    return response.data is not None


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------

def update_department(
    department_id: UUID,
    organization_id: UUID,
    data: dict[str, Any],
) -> dict:
    """
    Update a department.
    """

    response = (
        supabase
        .table(TABLE_NAME)
        .update(data)
        .eq("id", str(department_id))
        .eq("organization_id", str(organization_id))
        .execute()
    )

    return response.data[0]


# ---------------------------------------------------------
# Soft Delete
# ---------------------------------------------------------

def soft_delete_department(
    department_id: UUID,
    organization_id: UUID,
    data: dict[str, Any],
) -> dict:
    """
    Soft delete a department.
    """

    response = (
        supabase
        .table(TABLE_NAME)
        .update(data)
        .eq("id", str(department_id))
        .eq("organization_id", str(organization_id))
        .execute()
    )

    return response.data[0]