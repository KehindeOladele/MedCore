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

    return response.data

# ---------------------------------------------------------
# Get Department by ID
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

    return response.data if response.data else None 


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

    return response.data or []


# ---------------------------------------------------------
# Root Departments
# ---------------------------------------------------------

def get_root_departments(
    organization_id: UUID,
) -> list[dict]:
    """
    Retrieve all root-level departments for an organization.

    Root departments are departments without a parent.
    """

    response = (
        supabase
        .table(TABLE_NAME)
        .select("*")
        .eq("organization_id", str(organization_id))
        .is_("parent_department_id", "null")
        .is_("deleted_at", "null")
        .order("name")
        .execute()
    )

    return response.data[0] if response.data else None


# ---------------------------------------------------------
# Department Children
# ---------------------------------------------------------

def list_department_children(
    organization_id: UUID,
    parent_department_id: UUID,
) -> list[dict]:
    """
    Retrieve all direct child departments.
    """

    response = (
        supabase
        .table(TABLE_NAME)
        .select("*")
        .eq("organization_id", str(organization_id))
        .eq(
            "parent_department_id",
            str(parent_department_id),
        )
        .is_("deleted_at", "null")
        .order("name")
        .execute()
    )

    return response.data or []


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

    return bool(response.data)


# ---------------------------------------------------------
# Has Child Departments
# ---------------------------------------------------------

def has_child_departments(
    organization_id: UUID,
    department_id: UUID,
) -> bool:
    """
    Determine whether a department has any child departments.
    """

    children = list_department_children(
        organization_id,
        department_id,
    )
    return bool(children)


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

    return response.data if response.data else None


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

    return response.data if response.data else None