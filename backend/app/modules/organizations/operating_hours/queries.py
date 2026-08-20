"""Persistence-only helpers for organization operating hours."""

from typing import Any
from uuid import UUID

from app.core.supabase_client import supabase

from .constants import TABLE


def create_operating_hours(data: dict[str, Any]) -> dict[str, Any]:
    response = supabase.table(TABLE).insert(data).execute()
    return response.data[0]


def get_operating_hours(organization_id: UUID, operating_hours_id: UUID) -> dict[str, Any] | None:
    response = (
        supabase.table(TABLE).select("*")
        .eq("organization_id", str(organization_id))
        .eq("id", str(operating_hours_id))
        .is_("deleted_at", "null").limit(1).execute()
    )
    return response.data[0] if response.data else None


def list_operating_hours(organization_id: UUID, *, day_of_week: int | None = None) -> list[dict[str, Any]]:
    query = (
        supabase.table(TABLE).select("*")
        .eq("organization_id", str(organization_id))
        .is_("deleted_at", "null").order("day_of_week").order("slot_index")
    )
    if day_of_week is not None:
        query = query.eq("day_of_week", day_of_week)
    return query.execute().data or []


def update_operating_hours(organization_id: UUID, operating_hours_id: UUID, data: dict[str, Any]) -> dict[str, Any]:
    response = (
        supabase.table(TABLE).update(data)
        .eq("organization_id", str(organization_id))
        .eq("id", str(operating_hours_id)).execute()
    )
    return response.data[0]


def soft_delete_operating_hours(organization_id: UUID, operating_hours_id: UUID, data: dict[str, Any]) -> dict[str, Any]:
    return update_operating_hours(organization_id, operating_hours_id, data)
