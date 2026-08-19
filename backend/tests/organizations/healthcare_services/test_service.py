import pytest

from app.core.events.schemas import EventTypes

from app.modules.organizations.exceptions import (
    OrganizationNotFoundError,
    OrganizationInactiveError,
    DepartmentNotFoundError,
    DepartmentInactiveError,
)

from app.modules.organizations.healthcare_services import service

from app.modules.organizations.healthcare_services.exceptions import (
    HealthcareServiceNotFoundError,
    HealthcareServiceAlreadyExistsError,
)

from app.modules.organizations.healthcare_services.schemas import (
    HealthcareServiceResponse,
)

from tests.factories.constants import (
    ORGANIZATION_ID,
    HEALTHCARE_SERVICE_ID,
    USER_ID,
)

from tests.fixtures.healthcare_service import (
    healthcare_service_create,
    healthcare_service_update,
    healthcare_service_data
)

# ============================================================
# PRIVATE HELPER TESTS
# ============================================================


# ------------------------------------------------------------
# _get_healthcare_service_or_raise
# ------------------------------------------------------------

def test_get_healthcare_service_or_raise_found(
    mocker,
    healthcare_service_data,
):
    mocker.patch.object(
        service.queries,
        "get_healthcare_service",
        return_value=healthcare_service_data,
    )

    result = service._get_healthcare_service_or_raise(
        organization_id=ORGANIZATION_ID,
        healthcare_service_id=HEALTHCARE_SERVICE_ID,
    )

    assert result == healthcare_service_data


def test_get_healthcare_service_or_raise_not_found(
    mocker,
):
    mocker.patch.object(
        service.queries,
        "get_healthcare_service",
        return_value=None,
    )

    with pytest.raises(HealthcareServiceNotFoundError):
        service._get_healthcare_service_or_raise(
            organization_id=ORGANIZATION_ID,
            healthcare_service_id=HEALTHCARE_SERVICE_ID,
        )


# ------------------------------------------------------------
# _validate_organization_active
# ------------------------------------------------------------

def test_validate_organization_active_success(
    mocker,
):
    organization = {
        "id": ORGANIZATION_ID,
        "active": True,
    }

    mocker.patch.object(
        service.organization_queries,
        "get_organization",
        return_value=organization,
    )

    result = service._validate_organization_active(
        ORGANIZATION_ID
    )

    assert result == organization


def test_validate_organization_active_not_found(
    mocker,
):
    mocker.patch.object(
        service.organization_queries,
        "get_organization",
        return_value=None,
    )

    with pytest.raises(OrganizationNotFoundError):
        service._validate_organization_active(
            ORGANIZATION_ID
        )


def test_validate_organization_active_inactive(
    mocker,
):
    organization = {
        "id": ORGANIZATION_ID,
        "active": False,
    }

    mocker.patch.object(
        service.organization_queries,
        "get_organization",
        return_value=organization,
    )

    with pytest.raises(OrganizationInactiveError):
        service._validate_organization_active(
            ORGANIZATION_ID
        )


# ------------------------------------------------------------
# _validate_department
# ------------------------------------------------------------

def test_validate_department_none():
    result = service._validate_department(
        organization_id=ORGANIZATION_ID,
        department_id=None,
    )

    assert result is None


def test_validate_department_success(
    mocker,
):
    department = {
        "id": "department-id",
        "organization_id": ORGANIZATION_ID,
        "active": True,
    }

    mocker.patch.object(
        service.department_queries,
        "get_department",
        return_value=department,
    )

    result = service._validate_department(
        organization_id=ORGANIZATION_ID,
        department_id=UUID(
            "11111111-1111-1111-1111-111111111111"
        ),
    )

    assert result == department


def test_validate_department_not_found(
    mocker,
):
    mocker.patch.object(
        service.department_queries,
        "get_department",
        return_value=None,
    )

    with pytest.raises(DepartmentNotFoundError):
        service._validate_department(
            organization_id=ORGANIZATION_ID,
            department_id=UUID(
                "11111111-1111-1111-1111-111111111111"
            ),
        )


def test_validate_department_inactive(
    mocker,
):
    department = {
        "id": "department-id",
        "organization_id": ORGANIZATION_ID,
        "active": False,
    }

    mocker.patch.object(
        service.department_queries,
        "get_department",
        return_value=department,
    )

    with pytest.raises(DepartmentInactiveError):
        service._validate_department(
            organization_id=ORGANIZATION_ID,
            department_id=UUID(
                "11111111-1111-1111-1111-111111111111"
            ),
        )


# ------------------------------------------------------------
# _validate_unique_name
# ------------------------------------------------------------

def test_validate_unique_name_available(
    mocker,
):
    mocker.patch.object(
        service.queries,
        "get_healthcare_service_by_name",
        return_value=None,
    )

    service._validate_unique_name(
        organization_id=ORGANIZATION_ID,
        name="Cardiology",
    )


def test_validate_unique_name_duplicate(
    mocker,
):
    existing = {
        "id": HEALTHCARE_SERVICE_ID,
        "name": "Cardiology",
    }

    mocker.patch.object(
        service.queries,
        "get_healthcare_service_by_name",
        return_value=existing,
    )

    with pytest.raises(HealthcareServiceAlreadyExistsError):
        service._validate_unique_name(
            organization_id=ORGANIZATION_ID,
            name="Cardiology",
        )


def test_validate_unique_name_allows_excluded_service(
    mocker,
):
    existing = {
        "id": HEALTHCARE_SERVICE_ID,
        "name": "Cardiology",
    }

    mocker.patch.object(
        service.queries,
        "get_healthcare_service_by_name",
        return_value=existing,
    )

    service._validate_unique_name(
        organization_id=ORGANIZATION_ID,
        name="Cardiology",
        exclude_service_id=HEALTHCARE_SERVICE_ID,
    )


# ------------------------------------------------------------
# _prepare_create_payload
# ------------------------------------------------------------

def test_prepare_create_payload(
    healthcare_service_create,
):
    result = service._prepare_create_payload(
        organization_id=ORGANIZATION_ID,
        payload=healthcare_service_create,
        actor_id=USER_ID,
    )

    assert result["organization_id"] == ORGANIZATION_ID
    assert result["created_by"] == USER_ID
    assert result["updated_by"] == USER_ID
    assert result["name"] == healthcare_service_create.name


# ------------------------------------------------------------
# _prepare_update_payload
# ------------------------------------------------------------

def test_prepare_update_payload(
    healthcare_service_update,
):
    result = service._prepare_update_payload(
        payload=healthcare_service_update,
        actor_id=USER_ID,
    )

    assert result["updated_by"] == USER_ID
    assert result["name"] == healthcare_service_update.name


# ------------------------------------------------------------
# _build_healthcare_service_event_payload
# ------------------------------------------------------------

def test_build_healthcare_service_event_payload(
    healthcare_service_data,
):
    result = service._build_healthcare_service_event_payload(
        healthcare_service=healthcare_service_data,
        actor_id=USER_ID,
    )

    assert result == {
        "aggregate_type": "healthcare_service",
        "aggregate_id": HEALTHCARE_SERVICE_ID,
        "organization_id": ORGANIZATION_ID,
        "department_id": healthcare_service_data["department_id"],
        "actor_id": USER_ID,
        "service_name": healthcare_service_data["name"],
        "active": healthcare_service_data["active"],
    }


# ------------------------------------------------------------
# _emit_healthcare_service_event
# ------------------------------------------------------------

def test_emit_healthcare_service_event(
    mocker,
):
    emit_event = mocker.patch.object(
        service,
        "emit_event",
    )

    payload = {
        "aggregate_type": "healthcare_service",
        "aggregate_id": HEALTHCARE_SERVICE_ID,
    }

    service._emit_healthcare_service_event(
        event_type=EventTypes.HEALTHCARE_SERVICE_CREATED,
        payload=payload,
    )

    emit_event.assert_called_once_with(
        aggregate_type="healthcare_service",
        aggregate_id=HEALTHCARE_SERVICE_ID,
        event_type=EventTypes.HEALTHCARE_SERVICE_CREATED,
        payload=payload,
    )


# ============================================================
# CREATE SERVICE
# ============================================================

def test_create_healthcare_service_success(
    mocker,
    healthcare_service_create,
    healthcare_service_data,
):
    mocker.patch.object(
        service,
        "_validate_organization_active",
    )

    mocker.patch.object(
        service,
        "_validate_department",
    )

    mocker.patch.object(
        service,
        "_validate_unique_name",
    )

    create_query = mocker.patch.object(
        service.queries,
        "create_healthcare_service",
        return_value=healthcare_service_data,
    )

    activity = mocker.patch.object(
        service,
        "_record_healthcare_service_activity",
    )

    result = service.create_healthcare_service(
        organization_id=ORGANIZATION_ID,
        payload=healthcare_service_create,
        actor_id=USER_ID,
    )

    assert isinstance(
        result,
        HealthcareServiceResponse,
    )

    assert result.id == HEALTHCARE_SERVICE_ID

    create_query.assert_called_once()

    activity.assert_called_once_with(
        actor_id=USER_ID,
        action="healthcare_service.created",
        healthcare_service=healthcare_service_data,
        event_type=EventTypes.HEALTHCARE_SERVICE_CREATED,
    )


def test_create_healthcare_service_rejects_inactive_organization(
    mocker,
    healthcare_service_create,
):
    mocker.patch.object(
        service,
        "_validate_organization_active",
        side_effect=OrganizationInactiveError(),
    )

    with pytest.raises(OrganizationInactiveError):
        service.create_healthcare_service(
            organization_id=ORGANIZATION_ID,
            payload=healthcare_service_create,
            actor_id=USER_ID,
        )


def test_create_healthcare_service_rejects_duplicate_name(
    mocker,
    healthcare_service_create,
):
    mocker.patch.object(
        service,
        "_validate_organization_active",
    )

    mocker.patch.object(
        service,
        "_validate_department",
    )

    mocker.patch.object(
        service,
        "_validate_unique_name",
        side_effect=HealthcareServiceAlreadyExistsError(),
    )

    create_query = mocker.patch.object(
        service.queries,
        "create_healthcare_service",
    )

    with pytest.raises(HealthcareServiceAlreadyExistsError):
        service.create_healthcare_service(
            organization_id=ORGANIZATION_ID,
            payload=healthcare_service_create,
            actor_id=USER_ID,
        )

    create_query.assert_not_called()


# ============================================================
# GET SERVICE
# ============================================================

def test_get_healthcare_service_success(
    mocker,
    healthcare_service_data,
):
    mocker.patch.object(
        service,
        "_get_healthcare_service_or_raise",
        return_value=healthcare_service_data,
    )

    result = service.get_healthcare_service(
        organization_id=ORGANIZATION_ID,
        healthcare_service_id=HEALTHCARE_SERVICE_ID,
    )

    assert isinstance(
        result,
        HealthcareServiceResponse,
    )

    assert result.id == HEALTHCARE_SERVICE_ID


def test_get_healthcare_service_not_found(
    mocker,
):
    mocker.patch.object(
        service,
        "_get_healthcare_service_or_raise",
        side_effect=HealthcareServiceNotFoundError(),
    )

    with pytest.raises(HealthcareServiceNotFoundError):
        service.get_healthcare_service(
            organization_id=ORGANIZATION_ID,
            healthcare_service_id=HEALTHCARE_SERVICE_ID,
        )


# ============================================================
# LIST SERVICE
# ============================================================

def test_list_healthcare_services_success(
    mocker,
    healthcare_service_data,
):
    mocker.patch.object(
        service,
        "_validate_organization_active",
    )

    mocker.patch.object(
        service.queries,
        "list_healthcare_services",
        return_value=[healthcare_service_data],
    )

    result = service.list_healthcare_services(
        organization_id=ORGANIZATION_ID,
    )

    assert len(result) == 1

    assert isinstance(
        result[0],
        HealthcareServiceResponse,
    )

    assert result[0].id == UUID(HEALTHCARE_SERVICE_ID)


def test_list_healthcare_services_active_only(
    mocker,
    healthcare_service_data,
):
    mocker.patch.object(
        service,
        "_validate_organization_active",
    )

    list_query = mocker.patch.object(
        service.queries,
        "list_healthcare_services",
        return_value=[healthcare_service_data],
    )

    service.list_healthcare_services(
        organization_id=ORGANIZATION_ID,
        active_only=True,
    )

    list_query.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
        active_only=True,
    )


def test_list_healthcare_services_rejects_inactive_organization(
    mocker,
):
    mocker.patch.object(
        service,
        "_validate_organization_active",
        side_effect=OrganizationInactiveError(),
    )

    list_query = mocker.patch.object(
        service.queries,
        "list_healthcare_services",
    )

    with pytest.raises(OrganizationInactiveError):
        service.list_healthcare_services(
            organization_id=ORGANIZATION_ID,
        )

    list_query.assert_not_called()


# ============================================================
# UPDATE SERVICE
# ============================================================

def test_update_healthcare_service_success(
    mocker,
    healthcare_service_update,
    healthcare_service_data,
):
    mocker.patch.object(
        service,
        "_get_healthcare_service_or_raise",
        return_value=healthcare_service_data,
    )

    mocker.patch.object(
        service,
        "_validate_organization_active",
    )

    mocker.patch.object(
        service,
        "_validate_department",
    )

    mocker.patch.object(
        service,
        "_validate_unique_name",
    )

    update_query = mocker.patch.object(
        service.queries,
        "update_healthcare_service",
        return_value=healthcare_service_data,
    )

    activity = mocker.patch.object(
        service,
        "_record_healthcare_service_activity",
    )

    result = service.update_healthcare_service(
        organization_id=ORGANIZATION_ID,
        healthcare_service_id=HEALTHCARE_SERVICE_ID,
        payload=healthcare_service_update,
        actor_id=USER_ID,
    )

    assert isinstance(
        result,
        HealthcareServiceResponse,
    )

    update_query.assert_called_once()

    activity.assert_called_once_with(
        actor_id=USER_ID,
        action="healthcare_service.updated",
        healthcare_service=healthcare_service_data,
        event_type=EventTypes.HEALTHCARE_SERVICE_UPDATED,
    )


def test_update_healthcare_service_not_found(
    mocker,
    healthcare_service_update,
):
    mocker.patch.object(
        service,
        "_get_healthcare_service_or_raise",
        side_effect=HealthcareServiceNotFoundError(),
    )

    with pytest.raises(HealthcareServiceNotFoundError):
        service.update_healthcare_service(
            organization_id=ORGANIZATION_ID,
            healthcare_service_id=HEALTHCARE_SERVICE_ID,
            payload=healthcare_service_update,
            actor_id=USER_ID,
        )


def test_update_healthcare_service_duplicate_name(
    mocker,
    healthcare_service_update,
    healthcare_service_data,
):
    mocker.patch.object(
        service,
        "_get_healthcare_service_or_raise",
        return_value=healthcare_service_data,
    )

    mocker.patch.object(
        service,
        "_validate_organization_active",
    )

    mocker.patch.object(
        service,
        "_validate_department",
    )

    mocker.patch.object(
        service,
        "_validate_unique_name",
        side_effect=HealthcareServiceAlreadyExistsError(),
    )

    update_query = mocker.patch.object(
        service.queries,
        "update_healthcare_service",
    )

    with pytest.raises(HealthcareServiceAlreadyExistsError):
        service.update_healthcare_service(
            organization_id=ORGANIZATION_ID,
            healthcare_service_id=HEALTHCARE_SERVICE_ID,
            payload=healthcare_service_update,
            actor_id=USER_ID,
        )

    update_query.assert_not_called()


# ============================================================
# DELETE SERVICE
# ============================================================

def test_delete_healthcare_service_success(
    mocker,
    healthcare_service_data,
):
    mocker.patch.object(
        service,
        "_get_healthcare_service_or_raise",
        return_value=healthcare_service_data,
    )

    mocker.patch.object(
        service,
        "_validate_organization_active",
    )

    delete_query = mocker.patch.object(
        service.queries,
        "delete_healthcare_service",
    )

    activity = mocker.patch.object(
        service,
        "_record_healthcare_service_activity",
    )

    service.delete_healthcare_service(
        organization_id=ORGANIZATION_ID,
        healthcare_service_id=HEALTHCARE_SERVICE_ID,
        actor_id=USER_ID,
    )

    delete_query.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
        healthcare_service_id=HEALTHCARE_SERVICE_ID,
    )

    activity.assert_called_once()

    activity_call = activity.call_args.kwargs

    assert activity_call["actor_id"] == USER_ID
    assert activity_call["event_type"] == (
        EventTypes.HEALTHCARE_SERVICE_DELETED
    )

    assert activity_call["healthcare_service"]["active"] is False


def test_delete_healthcare_service_not_found(
    mocker,
):
    mocker.patch.object(
        service,
        "_get_healthcare_service_or_raise",
        side_effect=HealthcareServiceNotFoundError(),
    )

    delete_query = mocker.patch.object(
        service.queries,
        "delete_healthcare_service",
    )

    with pytest.raises(HealthcareServiceNotFoundError):
        service.delete_healthcare_service(
            organization_id=ORGANIZATION_ID,
            healthcare_service_id=HEALTHCARE_SERVICE_ID,
            actor_id=USER_ID,
        )

    delete_query.assert_not_called()


def test_delete_healthcare_service_inactive_organization(
    mocker,
    healthcare_service_data,
):
    mocker.patch.object(
        service,
        "_get_healthcare_service_or_raise",
        return_value=healthcare_service_data,
    )

    mocker.patch.object(
        service,
        "_validate_organization_active",
        side_effect=OrganizationInactiveError(),
    )

    delete_query = mocker.patch.object(
        service.queries,
        "delete_healthcare_service",
    )

    with pytest.raises(OrganizationInactiveError):
        service.delete_healthcare_service(
            organization_id=ORGANIZATION_ID,
            healthcare_service_id=HEALTHCARE_SERVICE_ID,
            actor_id=USER_ID,
        )

    delete_query.assert_not_called()