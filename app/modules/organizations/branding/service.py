from datetime import datetime, timezone
from uuid import UUID

from app.core.audit.service import log_audit_event
from app.core.events.emitter import emit_event
from app.core.events.schemas import EventTypes
from app.modules.organizations import queries as organization_queries
from app.modules.organizations.exceptions import OrganizationInactiveError, OrganizationNotFoundError

from . import queries, storage
from .exceptions import BrandingNotFoundError
from .schemas import BrandingResponse, BrandingThemeUpdate


def _validate_active_organization(organization_id: UUID) -> None:
    organization = organization_queries.get_organization(organization_id=organization_id)
    if organization is None:
        raise OrganizationNotFoundError()
    if not organization["active"]:
        raise OrganizationInactiveError()


def _response(record: dict) -> BrandingResponse:
    return BrandingResponse(
        organization_id=str(record["id"]), logo_url=record.get("logo_url"),
        primary_color=record.get("primary_color"), secondary_color=record.get("secondary_color"),
    )


def _record_activity(*, action: str, event_type: str, organization_id: UUID, actor_id: UUID, metadata: dict) -> None:
    log_audit_event(
        actor_id=str(actor_id), actor_type="user", organization_id=str(organization_id),
        action=action, resource_type="organization_branding", resource_id=str(organization_id), metadata=metadata,
    )
    emit_event(
        aggregate_type="organization", aggregate_id=str(organization_id), event_type=event_type,
        payload={"aggregate_type": "organization", "aggregate_id": str(organization_id), "organization_id": str(organization_id), "actor_id": str(actor_id), **metadata},
    )


def get_organization_branding(*, organization_id: UUID) -> BrandingResponse:
    _validate_active_organization(organization_id)
    branding = queries.get_branding(organization_id)
    if branding is None:
        raise BrandingNotFoundError()
    return _response(branding)


def update_theme(*, organization_id: UUID, payload: BrandingThemeUpdate, actor_id: UUID) -> BrandingResponse:
    _validate_active_organization(organization_id)
    updates = payload.model_dump(exclude_unset=True)
    updates["updated_at"] = datetime.now(timezone.utc).isoformat()
    branding = queries.update_branding(organization_id, updates)
    if branding is None:
        raise BrandingNotFoundError()
    _record_activity(action="organization.branding.updated", event_type=EventTypes.ORGANIZATION_BRANDING_UPDATED, organization_id=organization_id, actor_id=actor_id, metadata={"updated_fields": list(payload.model_fields_set)})
    return _response(branding)


def upload_logo(*, organization_id: UUID, content_type: str | None, content: bytes, actor_id: UUID) -> BrandingResponse:
    _validate_active_organization(organization_id)
    current = queries.get_branding(organization_id)
    if current is None:
        raise BrandingNotFoundError()
    path, url = storage.replace_logo(organization_id=organization_id, content_type=content_type, content=content)
    branding = queries.update_branding(organization_id, {"logo_path": path, "logo_url": url, "updated_at": datetime.now(timezone.utc).isoformat()})
    if branding is None:
        storage.delete_logo(path)
        raise BrandingNotFoundError()
    old_path = current.get("logo_path")
    if old_path and old_path != path:
        storage.delete_logo(old_path)
    _record_activity(action="organization.branding.logo_updated", event_type=EventTypes.ORGANIZATION_LOGO_UPDATED, organization_id=organization_id, actor_id=actor_id, metadata={"logo_path": path})
    return _response(branding)


def remove_logo(*, organization_id: UUID, actor_id: UUID) -> BrandingResponse:
    _validate_active_organization(organization_id)
    current = queries.get_branding(organization_id)
    if current is None:
        raise BrandingNotFoundError()
    if current.get("logo_path"):
        storage.delete_logo(current["logo_path"])
    branding = queries.update_branding(organization_id, {"logo_path": None, "logo_url": None, "updated_at": datetime.now(timezone.utc).isoformat()})
    if branding is None:
        raise BrandingNotFoundError()
    _record_activity(action="organization.branding.logo_removed", event_type=EventTypes.ORGANIZATION_LOGO_REMOVED, organization_id=organization_id, actor_id=actor_id, metadata={})
    return _response(branding)
