from uuid import UUID
from app.core.audit.service import log_audit_event
from app.core.events.schemas import EventTypes
from app.modules.organizations.departments import (
    queries as department_queries,
    )  

from . import queries
from app.core.events.emitter import emit_event
from .exceptions import (
    HealthcareServiceNotFoundError,
    HealthcareServiceAlreadyExistsError,
    )

from app.modules.organizations import queries as organization_queries
from app.modules.organizations.exceptions import (
    OrganizationNotFoundError,
    OrganizationInactiveError,
    DepartmentNotFoundError,
    DepartmentInactiveError,
    )
from .schemas import (
    HealthcareServiceCreate,
    HealthcareServiceUpdate,
    HealthcareServiceResponse
    )

# ----------------------------------------------------------------------------
# PRIVATE HELPERS
# ----------------------------------------------------------------------------

# ---------------------------------------------------
# GET HEALTHCARE SERVICE HELPER
# ---------------------------------------------------
def _get_healthcare_service_or_raise(
    *,
    organization_id: UUID,
    healthcare_service_id: UUID,
) -> dict:
    """
    Retrieve a healthcare service or raise an exception.

    Args:
        organization_id: Organization identifier.
        healthcare_service_id: Healthcare Service identifier.

    Raises:
        HealthcareServiceNotFoundError:
            If the healthcare service does not exist.

    Returns:
        Database record for the healthcare service.
    """

    healthcare_service = queries.get_healthcare_service(
        organization_id=organization_id,
        healthcare_service_id=healthcare_service_id,
    )

    if healthcare_service is None:
        raise HealthcareServiceNotFoundError()

    return healthcare_service




# ---------------------------------------------------
# VALIDATE ORGANIZATION EXIST HELPER
# ---------------------------------------------------
def _validate_organization_active(
    organization_id: UUID,
) -> dict:
    """
    Validate that the organization exists and is active.

    Returns:
        Organization record.

    Raises:
        OrganizationNotFoundError
        OrganizationInactiveError
    """

    organization = organization_queries.get_organization(
        organization_id=organization_id,
    )

    if organization is None:
        raise OrganizationNotFoundError()

    if not organization["active"]:
        raise OrganizationInactiveError()

    return organization


# ---------------------------------------------------
# VALIDATE DEPARTMENT EXIST HELPER
# ---------------------------------------------------
def _validate_department(
    *,
    organization_id: UUID,
    department_id: UUID | None,
) -> dict | None:
    """
    Validate department assignment.
    """

    if department_id is None:
        return None

    department = department_queries.get_department(
        organization_id=organization_id,
        department_id=department_id,
    )

    if department is None:
        raise DepartmentNotFoundError()

    if not department["active"]:
        raise DepartmentInactiveError()

    return department



# ---------------------------------------------------
# VALIDATE UNIQUE NAME HELPER
# ---------------------------------------------------
def _validate_unique_name(
    *,
    organization_id: UUID,
    name: str,
    exclude_service_id: UUID | None = None,
) -> None:
    """
    Validate that the service name is unique within an organization.
    """

    existing = queries.get_healthcare_service_by_name(
        organization_id=organization_id,
        name=name,
    )

    if existing is None:
        return

    if (
        exclude_service_id is not None
        and existing["id"] == str(exclude_service_id)
    ):
        return

    raise HealthcareServiceAlreadyExistsError()


# ---------------------------------------------------
# CREATE PAYLOAD HELPER
# ---------------------------------------------------
def _prepare_create_payload(
    *,
    organization_id: UUID,
    payload: HealthcareServiceCreate,
    actor_id: UUID,
) -> dict:
    """
    Prepare payload for database insertion.
    """

    data = payload.model_dump(
        exclude_none=True,
    )

    data["organization_id"] = str(organization_id)
    data["created_by"] = str(actor_id)
    data["updated_by"] = str(actor_id)

    return data


# ---------------------------------------------------
# PREPARE PAULOAD HELPER
# ---------------------------------------------------
def _prepare_update_payload(
    *,
    payload: HealthcareServiceUpdate,
    actor_id: UUID,
) -> dict:
    """
    Prepare update payload.
    """

    data = payload.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    data["updated_by"] = str(actor_id)

    return data


# ---------------------------------------------------
# PREPARE PAULOAD HELPER
# ---------------------------------------------------
def _log_healthcare_service_audit(
    *,
    actor_id: UUID,
    action: str,
    healthcare_service: dict,
) -> None:
    log_audit_event(
        actor_id=str(actor_id),
        actor_type="user",
        organization_id=str(
            healthcare_service["organization_id"]
        ),
        action=action,
        resource_type="healthcare_service",
        resource_id=str(
            healthcare_service["id"]
        ),
        metadata={
            "service_name": healthcare_service["name"],
        },
    )


# ---------------------------------------------------
# BUILD HEALTHCARE SERVICE EVENT PAYLOAD HELPER
# ---------------------------------------------------
def _build_healthcare_service_event_payload(
    *,
    healthcare_service: dict,
    actor_id: UUID,
) -> dict:
    """
    Build the event payload for healthcare service events.
    """

    return {
        "aggregate_type": "healthcare_service",
        "aggregate_id": healthcare_service["id"],
        "organization_id": healthcare_service["organization_id"],
        "department_id": healthcare_service.get("department_id"),
        "actor_id": str(actor_id),
        "service_name": healthcare_service["name"],
        "active": healthcare_service["active"],
    }


# ---------------------------------------------------
# BUILD HEALTHCARE SERVICE EVENT PAYLOAD HELPER
# ---------------------------------------------------
def _emit_healthcare_service_event(
    *,
    event_type: str,
    payload: dict,
) -> None:

    emit_event(
        aggregate_type=payload["aggregate_type"],
        aggregate_id=payload["aggregate_id"],
        event_type=event_type,
        payload=payload,
    )


# ---------------------------------------------------
# RECORD HEALTHCARE SERVICE ACTIVITY HELPER
# ---------------------------------------------------
def _record_healthcare_service_activity(
    *,
    action: str,
    event_type: str,
    healthcare_service: dict,
    actor_id: UUID,
) -> None:
    """
    Record audit information and emit the corresponding domain event.
    """

    _log_healthcare_service_audit(
        actor_id=actor_id,
        action=action,
        healthcare_service=healthcare_service,
    )

    payload = _build_healthcare_service_event_payload(
        healthcare_service=healthcare_service,
        actor_id=actor_id,
    )

    _emit_healthcare_service_event(
        event_type=event_type,
        payload=payload,
    )




# ----------------------------------------------------------------------------
# PUBLIC SERVICES
# ----------------------------------------------------------------------------



# ---------------------------------------------------------
# CREATE HEALTHCARE SERVICE
# ---------------------------------------------------------
def create_healthcare_service(
    *,
    organization_id: UUID,
    payload: HealthcareServiceCreate,
    actor_id: UUID,
) -> HealthcareServiceResponse:
    """
    Create a new healthcare service.
    """

    _validate_organization_active(
        organization_id,
    )

    _validate_department(
        organization_id=organization_id,
        department_id=payload.department_id,
    )

    _validate_unique_name(
        organization_id=organization_id,
        name=payload.name,
    )

    service_data = _prepare_create_payload(
        organization_id=organization_id,
        payload=payload,
        actor_id=actor_id,
    )

    healthcare_service = queries.create_healthcare_service(
        service_data,
        payload=payload
    )

    _record_healthcare_service_activity(
        actor_id=actor_id,
        action="healthcare_service.created",
        healthcare_service=healthcare_service,
        event_type=EventTypes.HEALTHCARE_SERVICE_CREATED,
    )

    return HealthcareServiceResponse.model_validate(
        healthcare_service
    )


# ---------------------------------------------------------
# GET HEALTHCARE SERVICE
# ---------------------------------------------------------
def get_healthcare_service(
    *,
    organization_id: UUID,
    healthcare_service_id: UUID,
) -> HealthcareServiceResponse:
    """
    Retrieve a healthcare service.
    """

    healthcare_service = (
        _get_healthcare_service_or_raise(
            organization_id=organization_id,
            healthcare_service_id=healthcare_service_id,
        )
    )

    return HealthcareServiceResponse.model_validate(
        healthcare_service
    )


# ---------------------------------------------------------
# LIST HEALTHCARE SERVICE
# ---------------------------------------------------------
def list_healthcare_services(
    *,
    organization_id: UUID,
    active_only: bool = False,
) -> list[HealthcareServiceResponse]:
    """
    List healthcare services.
    """

    _validate_organization_active(
        organization_id,
    )

    services = queries.list_healthcare_services(
        organization_id=organization_id,
        active_only=active_only,
    )

    return [
        HealthcareServiceResponse.model_validate(service)
        for service in services
    ]


# ---------------------------------------------------------
# UPDATE HEALTHCARE SERVICE
# ---------------------------------------------------------
def update_healthcare_service(
    *,
    organization_id: UUID,
    healthcare_service_id: UUID,
    payload: HealthcareServiceUpdate,
    actor_id: UUID,
) -> HealthcareServiceResponse:
    """
    Update a healthcare service.
    """

    existing = _get_healthcare_service_or_raise(
        organization_id=organization_id,
        healthcare_service_id=healthcare_service_id,
    )

    _validate_organization_active(
        organization_id,
    )

    department_id = (
        payload.department_id
        if payload.department_id is not None
        else existing.get("department_id")
    )

    _validate_department(
        organization_id=organization_id,
        department_id=department_id,
    )

    if payload.name is not None:
        _validate_unique_name(
            organization_id=organization_id,
            name=payload.name,
            exclude_service_id=healthcare_service_id,
        )

    update_data = _prepare_update_payload(
        payload=payload,
        actor_id=actor_id,
    )

    healthcare_service = (
        queries.update_healthcare_service(
            organization_id=organization_id,
            healthcare_service_id=healthcare_service_id,
            payload=payload
        )
    )

    _record_healthcare_service_activity(
        actor_id=actor_id,
        action= "healthcare_service.updated",
        healthcare_service=healthcare_service,
        event_type=EventTypes.HEALTHCARE_SERVICE_UPDATED,
    )

    return HealthcareServiceResponse.model_validate(
        healthcare_service
    )


# ---------------------------------------------------------
# DELETE HEALTHCARE SERVICE
# ---------------------------------------------------------
def delete_healthcare_service(
    *,
    organization_id: UUID,
    healthcare_service_id: UUID,
    actor_id: UUID,
) -> None:
    """
    Soft delete a healthcare service.
    """

    healthcare_service = (
        _get_healthcare_service_or_raise(
            organization_id=organization_id,
            healthcare_service_id=healthcare_service_id,
        )
    )

    _validate_organization_active(
        organization_id,
    )

    queries.delete_healthcare_service(
        organization_id=organization_id,
        healthcare_service_id=healthcare_service_id,
    )

    healthcare_service["active"] = False

    _record_healthcare_service_activity(
        actor_id=actor_id,
        action="healthcare_service.updated",
        healthcare_service=healthcare_service,
        event_type=EventTypes.HEALTHCARE_SERVICE_DELETED,
    )