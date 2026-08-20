"""Persistence-only helpers for organization branding."""

from typing import Any
from uuid import UUID

from app.core.supabase_admin import supabase_admin


def get_branding(organization_id: UUID) -> dict[str, Any] | None:
    response = (
        supabase_admin.table("organizations")
        .select("id, logo_url, logo_path, primary_color, secondary_color")
        .eq("id", str(organization_id)).maybe_single().execute()
    )
    return response.data or None


def update_branding(organization_id: UUID, updates: dict[str, Any]) -> dict[str, Any] | None:
    response = (
        supabase_admin.table("organizations").update(updates)
        .eq("id", str(organization_id))
        .select("id, logo_url, logo_path, primary_color, secondary_color")
        .maybe_single().execute()
    )
    return response.data or None
