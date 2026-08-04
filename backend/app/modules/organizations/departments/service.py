from datetime import datetime, timezone
from uuid import UUID

from app.core.audit.service import log_audit_event
from app.core.events.emitter import emit_event
from app.core.events.schemas import EventTypes

from .exceptions import (
    CircularDepartmentHierarchyError,
    DepartmentAlreadyExistsError,
    DepartmentHasChildrenError,
    InvalidParentDepartmentError,
)
from app.modules.organizations.exceptions import DepartmentNotFoundError

from .queries import (
    create_department,
    department_exists,
    get_department,
    get_root_departments,
    has_child_departments,
    list_department_children,
    list_departments,
    soft_delete_department,
    update_department,
)

from .schemas import (
    DepartmentUpdate,
    DepartmentCreate,
    DepartmentResponse
)


# ---------------------------------------------------------
# PRIVATE HELPERS
# ---------------------------------------------------------


# This helper will probably become the most used function in the module.
def _get_department_or_raise(
    organization_id: UUID,
    department_id: UUID,
) -> dict:
    """
    Retrieve a department or raise DepartmentNotFoundError.
    """

    department = get_department(
        organization_id=organization_id,
        department_id=department_id,
    )

    if department is None:
        raise DepartmentNotFoundError()

    return department


# This prevents invalid parent references.
def _validate_parent_department(
    organization_id: UUID,
    parent_department_id: UUID | None,
) -> None:
    """
    Validate the parent department exists.
    """

    if parent_department_id is None:
        return

    parent = get_department(
        organization_id=organization_id,
        department_id=parent_department_id,
    )

    if parent is None:
        raise InvalidParentDepartmentError()


# Validate Organization department
def _validate_department_name(
    organization_id: UUID,
    name: str,
) -> None:
    """
    Ensure department name is unique within an organization.
    """

    if department_exists(
        organization_id=organization_id,
        name=name,
    ):
        raise DepartmentAlreadyExistsError()



# This makes sure there is linear hierarchy
def _validate_no_circular_reference(
    organization_id: UUID,
    department_id: UUID,
    parent_department_id: UUID | None,
) -> None:
    """
    Prevent circular department hierarchies.
    """

    if parent_department_id is None:
        return

    current_parent = parent_department_id

    while current_parent is not None:

        if current_parent == department_id:
            raise CircularDepartmentHierarchyError()

        parent = get_department(
            organization_id=organization_id,
            department_id=current_parent,
        )

        if parent is None:
            break

        current_parent = parent.get("parent_department_id")


# Deletion rules belong together.
def _validate_department_deletion(
    organization_id: UUID,
    department_id: UUID,
) -> None:
    """
    Ensure a department can be deleted.
    """

    if has_child_departments(
        organization_id=organization_id,
        department_id=department_id,
    ):
        raise DepartmentHasChildrenError()

    #
    # Future-proof hooks for other modules
    #-------------------

    # if practitioners_exist(...):
    #     raise DepartmentInUseError()

    # if healthcare_services_exist(...):
    #     raise DepartmentInUseError()


# Central Logging for Departments
def _log_department_audit(
    *,
    actor_id: UUID,
    action: str,
    department: dict,
):
    """
    Record a department audit event.
    """

    log_audit_event(
        actor_id=str(actor_id),
        action=action,
        resource_type="department",
        resource_id=str(department["id"]),
        metadata={
            "organization_id": str(
                department["organization_id"]
            ),
            "department_name": department["name"],
        },
    )


# This helps prepare department update payload
def _prepare_department_update_payload(
    payload: DepartmentUpdate,
    actor_id: UUID,
) -> dict:
    """
    Prepare a department update payload for persistence.
    """

    update_data = payload.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    update_data["updated_at"] = datetime.now(timezone.utc)
    update_data["updated_by"] = str(actor_id)

    return update_data


# This helps to normalize deparment creation payload
def _prepare_department_create_payload(
    *,
    organization_id: UUID,
    payload: DepartmentCreate,
    actor_id: UUID,
) -> dict:
    """
    Prepare a department create payload for persistence.
    """

    department_data = payload.model_dump(exclude_none=True)

    department_data.update(
        {
            "organization_id": str(organization_id),
            "created_by": str(actor_id),
            "updated_by": str(actor_id),
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
    )

    return department_data


# This helper is responsible for constructing a standardized event payload.
def _build_department_event_payload(
    *,
    department: dict,
    actor_id: UUID,
) -> dict:
    """
    Build a standardized Department domain event payload.
    """

    return {
        # Aggregate metadata
        "aggregate_type": "department",
        "aggregate_id": str(department["id"]),

        # Domain data
        "department_id": str(department["id"]),
        "organization_id": str(department["organization_id"]),
        "parent_department_id": (
            str(department["parent_department_id"])
            if department.get("parent_department_id")
            else None
        ),
        "name": department["name"],
        "code": department.get("code"),
        "description": department.get("description"),
        "active": department["active"],

        # Event metadata
        "actor_id": str(actor_id),
        "occurred_at": department["updated_at"],
    }


# Central Event Emitter for Department
def _emit_department_event(
    *,
    event_type: EventTypes,
    actor_id: UUID,
    department: dict,
):
    """
    Publish a department domain event.
    """

    emit_event(
        event_type=event_type,
        aggregate_id=str(department["id"]),
        payload={
            "organization_id": str(
                department["organization_id"]
            ),
            "department_id": str(department["id"]),
            "department_name": department["name"],
            "actor_id": str(actor_id),
        },
    )




# ---------------------------------------------------------
# PUBLIC SERVICE
# ---------------------------------------------------------


# -------------------------
# Create Department Service
# -------------------------
def create_department_service(
    *,
    organization_id: UUID,
    payload: DepartmentCreate,
    actor_id: UUID,
) -> DepartmentResponse:
    """
    Create a new department.
    """

    _validate_department_name(
        organization_id=organization_id,
        name=payload.name,
    )

    _validate_parent_department(
        organization_id=organization_id,
        parent_department_id=payload.parent_department_id,
    )

    department_data = _prepare_department_create_payload(
        organization_id=organization_id,
        payload=payload,
        actor_id=actor_id,
    )

    department = create_department(department_data)

    _log_department_audit(
        actor_id=actor_id,
        action="department.created",
        department=department,
    )

    _emit_department_event(
        event_type=EventTypes.DEPARTMENT_CREATED,
        actor_id=actor_id,
        department=department,
    )

    return DepartmentResponse.model_validate(department)


# ----------------------
# Get Department Service
# ----------------------
def get_department_service(
    *,
    organization_id: UUID,
    department_id: UUID,
) -> DepartmentResponse:
    """
    Retrieve a department.
    """

    department = _get_department_or_raise(
        organization_id=organization_id,
        department_id=department_id,
    )

    return DepartmentResponse.model_validate(department)


# -----------------------
# List Department Service
# -----------------------
def list_departments_service(
    *,
    organization_id: UUID,
) -> list[DepartmentResponse]:
    """
    List all departments for an organization.
    """

    departments = list_departments(
        organization_id=organization_id,
    )

    return [
        DepartmentResponse.model_validate(department)
        for department in departments
    ]


# -------------------------
# Update Department Service
# -------------------------
def update_department_service(
    *,
    organization_id: UUID,
    department_id: UUID,
    payload: DepartmentUpdate,
    actor_id: UUID,
) -> DepartmentResponse:
    """
    Update a department.
    """

    department = _get_department_or_raise(
        organization_id=organization_id,
        department_id=department_id,
    )

    if (
        payload.name
        and payload.name != department["name"]
    ):
        _validate_department_name(
            organization_id=organization_id,
            name=payload.name,
        )

    if payload.parent_department_id is not None:

        _validate_parent_department(
            organization_id=organization_id,
            parent_department_id=payload.parent_department_id,
        )

        _validate_no_circular_reference(
            organization_id=organization_id,
            department_id=department_id,
            parent_department_id=payload.parent_department_id,
        )

    update_data = _prepare_department_update_payload(
        payload=payload,
        actor_id=actor_id,
    )

    updated = update_department(
        department_id=department_id,
        organization_id=organization_id,
        data=update_data,
    )

    _log_department_audit(
        actor_id=actor_id,
        action="department.updated",
        department=updated,
    )

    _emit_department_event(
        event_type=EventTypes.DEPARTMENT_UPDATED,
        actor_id=actor_id,
        department=updated,
    )

    return DepartmentResponse.model_validate(updated)


# -------------------------
# Delete Department Service
# -------------------------
def delete_department_service(
    *,
    organization_id: UUID,
    department_id: UUID,
    actor_id: UUID,
) -> None:
    """
    Soft delete a department.
    """

    department = _get_department_or_raise(
        organization_id=organization_id,
        department_id=department_id,
    )

    _validate_department_deletion(
        organization_id=organization_id,
        department_id=department_id,
    )

    deleted = soft_delete_department(
        department_id=department_id,
        organization_id=organization_id,
        data={
            "deleted_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "updated_by": str(actor_id),
            "active": False,
        },
    )

    _log_department_audit(
        actor_id=actor_id,
        action="department.deleted",
        department=deleted,
    )

    _emit_department_event(
        event_type=EventTypes.DEPARTMENT_DELETED,
        actor_id=actor_id,
        department=deleted,
    )



