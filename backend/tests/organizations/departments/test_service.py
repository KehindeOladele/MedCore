import pytest
from uuid import uuid4
from unittest.mock import ANY

from app.core.events.schemas import EventTypes

from app.modules.organizations.departments import service

from app.modules.organizations.departments.exceptions import (
    DepartmentAlreadyExistsError,
    InvalidParentDepartmentError,
    DepartmentHasChildrenError,
    DepartmentNotFoundError,
    CircularDepartmentHierarchyError
)

from app.modules.organizations.departments.schemas import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate
)

from tests.fixtures.departments import create_payload



ORGANIZATION_ID = uuid4()
ACTOR_ID = uuid4()



# ----------------------
# DUPLICATE PATCH HELPER
# ----------------------
def patch_service_side_effects(
    mocker,
    department_data,
):
    """
    Patch audit logging and event emission.
    """

    audit = mocker.patch.object(
        service,
        "_log_department_audit",
    )

    event = mocker.patch.object(
        service,
        "_emit_department_event",
    )

    create = mocker.patch.object(
        service,
        "create_department",
        return_value=department_data,
    )

    return audit, event, create



# ------------------------------
# CREATE DEPARTMEMT SERVICE TEST
# ------------------------------
def test_create_department_service_success(
    mocker,
    create_payload,
    department_data,
):

    mocker.patch.object(
        service,
        "_validate_department_name",
    )

    mocker.patch.object(
        service,
        "_validate_parent_department",
    )

    mocker.patch.object(
        service,
        "_prepare_department_create_payload",
        return_value=department_data,
    )

    audit, event, create = patch_service_side_effects(
        mocker,
        department_data,
    )

    result = service.create_department_service(
        organization_id=ORGANIZATION_ID,
        payload=create_payload,
        actor_id=ACTOR_ID,
    )

    create.assert_called_once_with(department_data)

    audit.assert_called_once()

    event.assert_called_once_with(
        event_type=EventTypes.DEPARTMENT_CREATED,
        actor_id=ACTOR_ID,
        department=department_data,
    )

    assert isinstance(result, DepartmentResponse)

    assert result.name == department_data["name"]


# -------------------------------------
# DUPLICATE DEPARMENT NAME SERVICE TEST
# -------------------------------------
def test_create_department_service_duplicate_name(
    mocker,
    create_payload,
):

    mocker.patch.object(
        service,
        "_validate_department_name",
        side_effect=DepartmentAlreadyExistsError(),
    )

    with pytest.raises(
        DepartmentAlreadyExistsError
    ):

        service.create_department_service(
            organization_id=ORGANIZATION_ID,
            payload=create_payload,
            actor_id=ACTOR_ID,
        )


# -------------------------------------
# CREATE DEPARMENT INVALID SERVICE TEST
# -------------------------------------
def test_create_department_service_invalid_parent(
    mocker,
    create_payload,
):

    mocker.patch.object(
        service,
        "_validate_department_name",
    )

    mocker.patch.object(
        service,
        "_validate_parent_department",
        side_effect=InvalidParentDepartmentError(),
    )

    with pytest.raises(
        InvalidParentDepartmentError
    ):

        service.create_department_service(
            organization_id=ORGANIZATION_ID,
            payload=create_payload,
            actor_id=ACTOR_ID,
        )


# ---------------------------------------
# CREATE DEPARMENT LOG AUDIT SERVICE TEST
# ---------------------------------------
def test_create_department_service_logs_audit(
    mocker,
    create_payload,
    department_data,
):

    mocker.patch.object(
        service,
        "_validate_department_name",
    )

    mocker.patch.object(
        service,
        "_validate_parent_department",
    )

    mocker.patch.object(
        service,
        "_prepare_department_create_payload",
        return_value=department_data,
    )

    audit, _, _ = patch_service_side_effects(
        mocker,
        department_data,
    )

    service.create_department_service(
        organization_id=ORGANIZATION_ID,
        payload=create_payload,
        actor_id=ACTOR_ID,
    )

    audit.assert_called_once_with(
        actor_id=ACTOR_ID,
        action="department.created",
        department=department_data,
    )


# ---------------------------------------
# CREATE DEPARMENT EMIT EVENT TEST
# ---------------------------------------
def test_create_department_service_emits_event(
    mocker,
    create_payload,
    department_data,
):

    mocker.patch.object(
        service,
        "_validate_department_name",
    )

    mocker.patch.object(
        service,
        "_validate_parent_department",
    )

    mocker.patch.object(
        service,
        "_prepare_department_create_payload",
        return_value=department_data,
    )

    _, event, _ = patch_service_side_effects(
        mocker,
        department_data,
    )

    service.create_department_service(
        organization_id=ORGANIZATION_ID,
        payload=create_payload,
        actor_id=ACTOR_ID,
    )

    event.assert_called_once_with(
        event_type=EventTypes.DEPARTMENT_CREATED,
        actor_id=ACTOR_ID,
        department=department_data,
    )


# ---------------------------------------
# GET DEPARTMENT SERVICE TEST
# ---------------------------------------
def test_get_department_service_success(
    mocker,
    department_data,
):
    mocker.patch.object(
        service,
        "_get_department_or_raise",
        return_value=department_data,
    )

    result = service.get_department_service(
        organization_id=ORGANIZATION_ID,
        department_id=department_data["id"],
    )

    service._get_department_or_raise.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
        department_id=department_data["id"],
    )

    assert isinstance(result, DepartmentResponse)
    assert result.id == department_data["id"]
    assert result.name == department_data["name"]


# ---------------------------------------
# GET DEPARTMENT SERVICE NOT FOUND TEST
# ---------------------------------------
def test_get_department_service_not_found(
    mocker,
):
    mocker.patch.object(
        service,
        "_get_department_or_raise",
        side_effect=service.DepartmentNotFoundError(),
    )

    with pytest.raises(service.DepartmentNotFoundError):
        service.get_department_service(
            organization_id=ORGANIZATION_ID,
            department_id=uuid4(),
        )


# ---------------------------------------
# LIST DEPARTMENTS SERVICE TEST
# ---------------------------------------
def test_list_departments_service_success(
    mocker,
    department_data,
):
    mocker.patch.object(
        service,
        "list_departments",
        return_value=[department_data],
    )

    result = service.list_departments_service(
        organization_id=ORGANIZATION_ID,
    )

    service.list_departments.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
    )

    assert len(result) == 1
    assert isinstance(result[0], DepartmentResponse)
    assert result[0].name == department_data["name"]


# ---------------------------------------
# LIST DEPARTMENTS SERVICE EMPTY TEST
# ---------------------------------------
def test_list_departments_service_empty(
    mocker,
):
    mocker.patch.object(
        service,
        "list_departments",
        return_value=[],
    )

    result = service.list_departments_service(
        organization_id=ORGANIZATION_ID,
    )

    assert result == []


# ---------------------------------------
# UPDATE DEPARTMENT SUCCESS SERVICE TEST
# ---------------------------------------
def test_update_department_service_success(
    mocker,
    department_data,
    updated_department_data,
    update_payload,
):
    mocker.patch.object(
        service,
        "_get_department_or_raise",
        return_value=department_data,
    )

    validate_name = mocker.patch.object(
        service,
        "_validate_department_name",
    )

    validate_parent = mocker.patch.object(
        service,
        "_validate_parent_department",
    )

    validate_hierarchy = mocker.patch.object(
        service,
        "_validate_no_circular_reference",
    )

    mocker.patch.object(
        service,
        "_prepare_department_update_payload",
        return_value=updated_department_data,
    )

    update = mocker.patch.object(
        service,
        "update_department",
        return_value=updated_department_data,
    )

    audit = mocker.patch.object(
        service,
        "_log_department_audit",
    )

    event = mocker.patch.object(
        service,
        "_emit_department_event",
    )

    result = service.update_department_service(
        organization_id=ORGANIZATION_ID,
        department_id=department_data["id"],
        payload=update_payload,
        actor_id=ACTOR_ID,
    )

    validate_name.assert_called_once()

    validate_parent.assert_not_called()

    validate_hierarchy.assert_not_called()

    update.assert_called_once()

    audit.assert_called_once()

    event.assert_called_once_with(
        event_type=EventTypes.DEPARTMENT_UPDATED,
        actor_id=ACTOR_ID,
        department=updated_department_data,
    )

    assert isinstance(result, DepartmentResponse)
    assert result.name == updated_department_data["name"]


# ---------------------------------------
# VALIDATE DEPARTMENT NAME SERVICE TEST
# ---------------------------------------
def test_update_department_service_duplicate_name(
    mocker,
    department_data,
    update_payload,
):
    mocker.patch.object(
        service,
        "_get_department_or_raise",
        return_value=department_data,
    )

    mocker.patch.object(
        service,
        "_validate_department_name",
        side_effect=DepartmentAlreadyExistsError(),
    )

    with pytest.raises(
        DepartmentAlreadyExistsError,
    ):
        service.update_department_service(
            organization_id=ORGANIZATION_ID,
            department_id=department_data["id"],
            payload=update_payload,
            actor_id=ACTOR_ID,
        )


# ---------------------------------------
# VALIDATE DEPARTMENT PARENT SERVICE TEST
# ---------------------------------------
def test_update_department_service_invalid_parent(
    mocker,
    department_data,
):
    payload = DepartmentUpdate(
        parent_department_id=uuid4(),
    )

    mocker.patch.object(
        service,
        "_get_department_or_raise",
        return_value=department_data,
    )

    mocker.patch.object(
        service,
        "_validate_parent_department",
        side_effect=InvalidParentDepartmentError(),
    )

    with pytest.raises(
        InvalidParentDepartmentError,
    ):
        service.update_department_service(
            organization_id=ORGANIZATION_ID,
            department_id=department_data["id"],
            payload=payload,
            actor_id=ACTOR_ID,
        )


# ---------------------------------------
# CIRCULAR HIERARCHY SERVICE TEST
# ---------------------------------------
def test_update_department_service_circular_reference(
    mocker,
    department_data,
):
    payload = DepartmentUpdate(
        parent_department_id=uuid4(),
    )

    mocker.patch.object(
        service,
        "_get_department_or_raise",
        return_value=department_data,
    )

    mocker.patch.object(
        service,
        "_validate_parent_department",
    )

    mocker.patch.object(
        service,
        "_validate_no_circular_reference",
        side_effect=service.CircularDepartmentHierarchyError(),
    )

    with pytest.raises(
        service.CircularDepartmentHierarchyError,
    ):
        service.update_department_service(
            organization_id=ORGANIZATION_ID,
            department_id=department_data["id"],
            payload=payload,
            actor_id=ACTOR_ID,
        )


# -----------------------------------------
# UPDATE DEPARTMENT NOT FOUND SERVICE TEST
# -----------------------------------------
def test_update_department_service_not_found(
    mocker,
    update_payload,
):
    mocker.patch.object(
        service,
        "_get_department_or_raise",
        side_effect=service.DepartmentNotFoundError(),
    )

    with pytest.raises(
        service.DepartmentNotFoundError,
    ):
        service.update_department_service(
            organization_id=ORGANIZATION_ID,
            department_id=uuid4(),
            payload=update_payload,
            actor_id=ACTOR_ID,
        )


# -----------------------------------------
# UPDATE DEPARTMENT AUDIT LOGS SERVICE TEST
# -----------------------------------------
def test_update_department_service_logs_audit(
    mocker,
    department_data,
    updated_department_data,
    update_payload,
):
    mocker.patch.object(
        service,
        "_get_department_or_raise",
        return_value=department_data,
    )

    mocker.patch.object(
        service,
        "_prepare_department_update_payload",
        return_value=updated_department_data,
    )

    mocker.patch.object(
        service,
        "update_department",
        return_value=updated_department_data,
    )

    audit = mocker.patch.object(
        service,
        "_log_department_audit",
    )

    mocker.patch.object(
        service,
        "_emit_department_event",
    )

    service.update_department_service(
        organization_id=ORGANIZATION_ID,
        department_id=department_data["id"],
        payload=update_payload,
        actor_id=ACTOR_ID,
    )

    audit.assert_called_once_with(
        actor_id=ACTOR_ID,
        action="department.updated",
        department=updated_department_data,
    )


# -----------------------------------------
# UPDATE DEPARTMENT EVENT SERVICE TEST
# -----------------------------------------
def test_update_department_service_emits_event(
    mocker,
    department_data,
    updated_department_data,
    update_payload,
):
    mocker.patch.object(
        service,
        "_get_department_or_raise",
        return_value=department_data,
    )

    mocker.patch.object(
        service,
        "_prepare_department_update_payload",
        return_value=updated_department_data,
    )

    mocker.patch.object(
        service,
        "update_department",
        return_value=updated_department_data,
    )

    mocker.patch.object(
        service,
        "_log_department_audit",
    )

    event = mocker.patch.object(
        service,
        "_emit_department_event",
    )

    service.update_department_service(
        organization_id=ORGANIZATION_ID,
        department_id=department_data["id"],
        payload=update_payload,
        actor_id=ACTOR_ID,
    )

    event.assert_called_once_with(
        event_type=EventTypes.DEPARTMENT_UPDATED,
        actor_id=ACTOR_ID,
        department=updated_department_data,
    )



# -----------------------------------------
# DELETE DEPARTMENT SERVICE TEST
# -----------------------------------------
def test_delete_department_service_success(
    mocker,
    department_data,
):
    mocker.patch.object(
        service,
        "_get_department_or_raise",
        return_value=department_data,
    )

    mocker.patch.object(
        service,
        "_validate_department_deletion",
    )

    deleted_department = {
        **department_data,
        "active": False,
    }

    delete = mocker.patch.object(
        service,
        "soft_delete_department",
        return_value=deleted_department,
    )

    audit = mocker.patch.object(
        service,
        "_log_department_audit",
    )

    event = mocker.patch.object(
        service,
        "_emit_department_event",
    )

    service.delete_department_service(
        organization_id=ORGANIZATION_ID,
        department_id=department_data["id"],
        actor_id=ACTOR_ID,
    )

    delete.assert_called_once()

    audit.assert_called_once_with(
        actor_id=ACTOR_ID,
        action="department.deleted",
        department=deleted_department,
    )

    event.assert_called_once_with(
        event_type=EventTypes.DEPARTMENT_DELETED,
        actor_id=ACTOR_ID,
        department=deleted_department,
    )



# --------------------------------------------
# DELETE DEPARTMENT HAS CHILDREN SERVICE TEST
# --------------------------------------------
def test_delete_department_service_has_children(
    mocker,
    department_data,
):
    mocker.patch.object(
        service,
        "_get_department_or_raise",
        return_value=department_data,
    )

    mocker.patch.object(
        service,
        "_validate_department_deletion",
        side_effect=DepartmentHasChildrenError(),
    )

    with pytest.raises(
        DepartmentHasChildrenError,
    ):
        service.delete_department_service(
            organization_id=ORGANIZATION_ID,
            department_id=department_data["id"],
            actor_id=ACTOR_ID,
        )  



# --------------------------------------------
# DELETE DEPARTMENT NOT FOUND SERVICE TEST
# --------------------------------------------
def test_delete_department_service_not_found(
    mocker,
):
    mocker.patch.object(
        service,
        "_get_department_or_raise",
        side_effect=DepartmentNotFoundError(),
    )

    with pytest.raises(
        DepartmentNotFoundError,
    ):
        service.delete_department_service(
            organization_id=ORGANIZATION_ID,
            department_id=uuid4(),
            actor_id=ACTOR_ID,
        )


# ---------------------------------------------
# PREPARE CREATE DEPARTMENT PAYLOAD HEPLER TEST
# ---------------------------------------------
def test_prepare_department_create_payload(
    create_payload,
):
    payload = service._prepare_department_create_payload(
        organization_id=ORGANIZATION_ID,
        payload=create_payload,
        actor_id=ACTOR_ID,
    )

    assert payload["organization_id"] == str(ORGANIZATION_ID)

    assert payload["created_by"] == str(ACTOR_ID)

    assert payload["updated_by"] == str(ACTOR_ID)

    assert "created_at" in payload

    assert "updated_at" in payload

    assert payload["name"] == create_payload.name



# ---------------------------------------------
# BUILD DEPARTMENT EVENT PAYLOAD HEPLER TEST
# ---------------------------------------------
def test_build_department_event_payload(
    department_data,
):
    payload = service._build_department_event_payload(
        department=department_data,
        actor_id=ACTOR_ID,
    )

    assert payload["aggregate_type"] == "department"

    assert payload["aggregate_id"] == str(
        department_data["id"]
    )

    assert payload["department_id"] == str(
        department_data["id"]
    )

    assert payload["organization_id"] == str(
        department_data["organization_id"]
    )

    assert payload["actor_id"] == str(
        ACTOR_ID
    )

    assert payload["name"] == department_data["name"]




# ---------------------------------------------
# GET DEPARTMENT SUCCESS HEPLER TEST
# ---------------------------------------------
def test_get_department_or_raise_success(
    mocker,
    department_data,
):
    mocker.patch.object(
        service,
        "get_department",
        return_value=department_data,
    )

    result = service._get_department_or_raise(
        organization_id=department_data["organization_id"],
        department_id=department_data["id"],
    )

    assert result == department_data


# ---------------------------------------------
# GET DEPARTMENT NOT FOUND HEPLER TEST
# ---------------------------------------------
def test_get_department_or_raise_not_found(
    mocker,
):
    mocker.patch.object(
        service,
        "get_department",
        return_value=None,
    )

    with pytest.raises(
        DepartmentNotFoundError,
    ):
        service._get_department_or_raise(
            organization_id=uuid4(),
            department_id=uuid4(),
        )


# ---------------------------------------------
# VALIDATE DEPARTMENT NAME SERVICE TEST
# ---------------------------------------------
def test_validate_department_name_success(
    mocker,
):
    mocker.patch.object(
        service,
        "department_exists",
        return_value=False,
    )

    service._validate_department_name(
        organization_id=uuid4(),
        name="Radiology",
    )



# -----------------------------------------------
# VALIDATE DEPARTMENT DUPLIVATE NAME SERVICE TEST
# -----------------------------------------------
def test_validate_department_name_duplicate(
    mocker,
):
    mocker.patch.object(
        service,
        "department_exists",
        return_value=True,
    )

    with pytest.raises(
        DepartmentAlreadyExistsError,
    ):
        service._validate_department_name(
            organization_id=uuid4(),
            name="Radiology",
        )



# -----------------------------------------------
# VALIDATE PARENT DEPARTMENT SUCCESS SERVICE TEST
# -----------------------------------------------
def test_validate_parent_department_success(
    mocker,
    department_data,
):
    mocker.patch.object(
        service,
        "get_department",
        return_value=department_data,
    )

    service._validate_parent_department(
        organization_id=department_data["organization_id"],
        parent_department_id=department_data["id"],
    )



# -------------------------------------------------
# VALIDATE PARENT DEPARTMENT NOT FOUND SERVICE TEST
# -------------------------------------------------
def test_validate_parent_department_not_found(
    mocker,
):
    mocker.patch.object(
        service,
        "get_department",
        return_value=None,
    )

    with pytest.raises(
        InvalidParentDepartmentError,
    ):
        service._validate_parent_department(
            organization_id=uuid4(),
            parent_department_id=uuid4(),
        )



# -------------------------------------------------
# VALIDATE CIRCULAR REFEREMCE SUCCESS SERVICE TEST
# -------------------------------------------------
def test_validate_no_circular_reference_success(
    mocker,
    department_data,
):
    mocker.patch.object(
        service,
        "get_department",
        return_value=None,
    )

    service._validate_no_circular_reference(
        organization_id=department_data["organization_id"],
        department_id=department_data["id"],
        parent_department_id=uuid4(),
    )



# -------------------------------------------------
# VALIDATE CIRCULAR REFEREMCE FAIL SERVICE TEST
# -------------------------------------------------
def test_validate_no_circular_reference_detects_cycle(
    mocker,
):
    department_id = uuid4()

    mocker.patch.object(
        service,
        "get_department",
        return_value={
            "parent_department_id": department_id,
        },
    )

    with pytest.raises(
        CircularDepartmentHierarchyError,
    ):
        service._validate_no_circular_reference(
            organization_id=uuid4(),
            department_id=department_id,
            parent_department_id=uuid4(),
        )



# -------------------------------------------------
# VALIDATE DEPARTMENT DELETE SUCCESS SERVICE TEST
# -------------------------------------------------
def test_validate_department_deletion_success(
    mocker,
):
    mocker.patch.object(
        service,
        "has_child_departments",
        return_value=False,
    )

    service._validate_department_deletion(
        organization_id=uuid4(),
        department_id=uuid4(),
    )


    
# -------------------------------------------------
# VALIDATE DEPARTMENT DELETION HAS CHILDREN TEST
# -------------------------------------------------
def test_validate_department_deletion_has_children(
    mocker,
):
    mocker.patch.object(
        service,
        "has_child_departments",
        return_value=True,
    )

    with pytest.raises(
        DepartmentHasChildrenError,
    ):
        service._validate_department_deletion(
            organization_id=uuid4(),
            department_id=uuid4(),
        )