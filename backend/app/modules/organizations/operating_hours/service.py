"""Business rules for organization operating hours."""

from datetime import datetime, time, timezone
from uuid import UUID

from app.core.audit.service import log_audit_event
from app.core.events.emitter import emit_event
from app.core.events.schemas import EventTypes
from app.modules.organizations import queries as organization_queries
from app.modules.organizations.exceptions import OrganizationInactiveError, OrganizationNotFoundError

from . import queries
from .exceptions import OperatingHoursConflictError, OperatingHoursNotFoundError
from .schemas import OperatingHoursBase, OperatingHoursCreate, OperatingHoursResponse, OperatingHoursUpdate


def _validate_organization_active(organization_id: UUID) -> None:
    organization = organization_queries.get_organization(organization_id=organization_id)
    if organization is None:
        raise OrganizationNotFoundError()
    if not organization["active"]:
        raise OrganizationInactiveError()


def _get_or_raise(organization_id: UUID, operating_hours_id: UUID) -> dict:
    entry = queries.get_operating_hours(organization_id, operating_hours_id)
    if entry is None:
        raise OperatingHoursNotFoundError()
    return entry


def _as_time(value: time | str | None) -> time | None:
    return time.fromisoformat(value) if isinstance(value, str) else value


def _validate_day_conflicts(*, organization_id: UUID, candidate: OperatingHoursBase, exclude_id: UUID | None = None) -> None:
    """Ensure one day cannot be closed and open, or contain overlapping windows."""
    for existing in queries.list_operating_hours(organization_id, day_of_week=candidate.day_of_week):
        if exclude_id is not None and str(existing["id"]) == str(exclude_id):
            continue
        # The database also enforces this, but catching it here preserves a
        # domain-level error instead of leaking a storage constraint failure.
        if existing["slot_index"] == candidate.slot_index:
            raise OperatingHoursConflictError()
        if candidate.is_closed or existing["is_closed"]:
            raise OperatingHoursConflictError()
        existing_opens = _as_time(existing["opens_at"])
        existing_closes = _as_time(existing["closes_at"])
        if candidate.opens_at < existing_closes and existing_opens < candidate.closes_at:
            raise OperatingHoursConflictError()


def _record_activity(*, action: str, event_type: str, entry: dict, actor_id: UUID) -> None:
    log_audit_event(
        actor_id=str(actor_id), actor_type="user", organization_id=str(entry["organization_id"]),
        action=action, resource_type="operating_hours", resource_id=str(entry["id"]),
        metadata={"day_of_week": entry["day_of_week"], "slot_index": entry["slot_index"], "is_closed": entry["is_closed"]},
    )
    payload = {
        "aggregate_type": "operating_hours", "aggregate_id": str(entry["id"]),
        "organization_id": str(entry["organization_id"]), "day_of_week": entry["day_of_week"],
        "slot_index": entry["slot_index"], "is_closed": entry["is_closed"], "actor_id": str(actor_id),
    }
    emit_event(aggregate_type=payload["aggregate_type"], aggregate_id=payload["aggregate_id"], event_type=event_type, payload=payload)


def create_operating_hours(*, organization_id: UUID, payload: OperatingHoursCreate, actor_id: UUID) -> OperatingHoursResponse:
    _validate_organization_active(organization_id)
    _validate_day_conflicts(organization_id=organization_id, candidate=payload)
    data = payload.model_dump(mode="json")
    data.update({"organization_id": str(organization_id), "created_by": str(actor_id), "updated_by": str(actor_id)})
    entry = queries.create_operating_hours(data)
    _record_activity(action="operating_hours.created", event_type=EventTypes.OPERATING_HOURS_CREATED, entry=entry, actor_id=actor_id)
    return OperatingHoursResponse.model_validate(entry)


def get_operating_hours(*, organization_id: UUID, operating_hours_id: UUID) -> OperatingHoursResponse:
    return OperatingHoursResponse.model_validate(_get_or_raise(organization_id, operating_hours_id))


def list_operating_hours(*, organization_id: UUID) -> list[OperatingHoursResponse]:
    _validate_organization_active(organization_id)
    return [OperatingHoursResponse.model_validate(entry) for entry in queries.list_operating_hours(organization_id)]


def update_operating_hours(*, organization_id: UUID, operating_hours_id: UUID, payload: OperatingHoursUpdate, actor_id: UUID) -> OperatingHoursResponse:
    _validate_organization_active(organization_id)
    existing = _get_or_raise(organization_id, operating_hours_id)
    values = {**existing, **payload.model_dump(exclude_unset=True)}
    candidate = OperatingHoursBase.model_validate({key: values[key] for key in ("day_of_week", "slot_index", "opens_at", "closes_at", "is_closed")})
    _validate_day_conflicts(organization_id=organization_id, candidate=candidate, exclude_id=operating_hours_id)
    updates = payload.model_dump(exclude_unset=True, mode="json")
    updates.update({"updated_by": str(actor_id), "updated_at": datetime.now(timezone.utc).isoformat()})
    entry = queries.update_operating_hours(organization_id, operating_hours_id, updates)
    _record_activity(action="operating_hours.updated", event_type=EventTypes.OPERATING_HOURS_UPDATED, entry=entry, actor_id=actor_id)
    return OperatingHoursResponse.model_validate(entry)


def delete_operating_hours(*, organization_id: UUID, operating_hours_id: UUID, actor_id: UUID) -> None:
    _validate_organization_active(organization_id)
    _get_or_raise(organization_id, operating_hours_id)
    entry = queries.soft_delete_operating_hours(organization_id, operating_hours_id, {
        "deleted_at": datetime.now(timezone.utc).isoformat(), "updated_at": datetime.now(timezone.utc).isoformat(), "updated_by": str(actor_id),
    })
    _record_activity(action="operating_hours.deleted", event_type=EventTypes.OPERATING_HOURS_DELETED, entry=entry, actor_id=actor_id)
