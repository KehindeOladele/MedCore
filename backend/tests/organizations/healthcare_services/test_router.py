import pytest
from uuid import uuid4

from app.modules.organizations.healthcare_services import router
from app.modules.organizations.healthcare_services.schemas import (
    HealthcareServiceResponse,
)
from app.modules.organizations.healthcare_services.exceptions import (
    HealthcareServiceNotFoundError,
)
from app.modules.organizations.exceptions import (
    OrganizationAccessDeniedError,
)
from tests.fixtures.auth import authenticated_user
from tests.fixtures.organizations import organization
from tests.factories.user import USER_ID
from tests.factories.organization import (
    HEALTHCARE_SERVICE_ID, 
    ORGANIZATION_ID
)
from app.modules.organizations.dependencies import (
    require_organization_access,
)




# --------------------------------------------
# CREATE HEALTHCARE SERVICE TEST
# --------------------------------------------

# CREATE SUCCESS
# --------------------------------------------
def test_create_healthcare_service_success(
    authenticated_client,
    mocker,
    healthcare_service_response,
):
    create_service = mocker.patch.object(
        router,
        "create_healthcare_service_service",
        return_value=healthcare_service_response,
    )

    response = authenticated_client.post(
        "/healthcare-services/",
        json={
            "name": "Cardiology",
            "description": "Cardiology services",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["name"] == "Cardiology"

    create_service.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
        payload=mocker.ANY,
        actor_id=USER_ID,
    )



# VALIDATE
# --------------------------------------------
def test_create_healthcare_service_invalid_payload(
    authenticated_client,
):
    response = authenticated_client.post(
        "/healthcare-services/",
        json={
            "name": "",
        },
    )

    assert response.status_code == 422


# --------------------------------------------
# GET SERVICE LIST TEST
# --------------------------------------------
def test_list_healthcare_services_success(
    authenticated_client,
    mocker,
    healthcare_service_response,
):
    list_service = mocker.patch.object(
        router,
        "list_healthcare_services_service",
        return_value=[
            healthcare_service_response
        ],
    )

    response = authenticated_client.get(
        "/healthcare-services/"
    )

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Cardiology"

    list_service.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
    )


# --------------------------------------------
# GET EMPTY SERVICE LIST TEST
# --------------------------------------------
def test_list_healthcare_services_empty(
    authenticated_client,
    mocker,
):
    mocker.patch.object(
        router,
        "list_healthcare_services_service",
        return_value=[],
    )

    response = authenticated_client.get(
        "/healthcare-services/"
    )

    assert response.status_code == 200
    assert response.json() == []



# --------------------------------------------
# GET SERVICE SUCCESS TEST
# --------------------------------------------
def test_get_healthcare_service_success(
    authenticated_client,
    mocker,
    healthcare_service_response,
):
    get_service = mocker.patch.object(
        router,
        "get_healthcare_service_service",
        return_value=healthcare_service_response,
    )

    response = authenticated_client.get(
        f"/healthcare-services/{HEALTHCARE_SERVICE_ID}"
    )

    assert response.status_code == 200

    get_service.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
        healthcare_service_id=HEALTHCARE_SERVICE_ID,
    )


# --------------------------------------------
# GET SERVICE EXCEPTION TEST
# --------------------------------------------
def test_get_healthcare_service_not_found(
    authenticated_client,
    mocker,
):
    mocker.patch.object(
        router,
        "get_healthcare_service_service",
        side_effect=HealthcareServiceNotFoundError(),
    )

    response = authenticated_client.get(
        f"/healthcare-services/{HEALTHCARE_SERVICE_ID}"
    )

    assert response.status_code == 404


# --------------------------------------------
# UPDATE HEALTHCARE SERVICE TEST
# --------------------------------------------
def test_update_healthcare_service_success(
    authenticated_client,
    mocker,
    healthcare_service_response,
):
    update_service = mocker.patch.object(
        router,
        "update_healthcare_service_service",
        return_value=healthcare_service_response,
    )

    response = authenticated_client.patch(
        f"/healthcare-services/{HEALTHCARE_SERVICE_ID}",
        json={
            "name": "Updated Cardiology",
        },
    )

    assert response.status_code == 200

    update_service.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
        healthcare_service_id=HEALTHCARE_SERVICE_ID,
        payload=mocker.ANY,
        actor_id=USER_ID,
    )



# --------------------------------------------
# DELATE HEALTHCARE SERVICE TEST
# --------------------------------------------
def test_delete_healthcare_service_success(
    authenticated_client,
    mocker,
):
    delete_service = mocker.patch.object(
        router,
        "delete_healthcare_service_service",
    )

    response = authenticated_client.delete(
        f"/healthcare-services/{HEALTHCARE_SERVICE_ID}"
    )

    assert response.status_code == 204
    assert response.content == b""

    delete_service.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
        healthcare_service_id=HEALTHCARE_SERVICE_ID,
        actor_id=USER_ID,
    )



# --------------------------------------------
# HEALTHCARE SERVICE AUTHENTICATION TEST
# --------------------------------------------
def test_list_healthcare_services_requires_authentication(
    client,
):
    response = client.get(
        "/healthcare-services/"
    )

    assert response.status_code == 401



def test_create_healthcare_service_requires_authentication(
    client,
):
    response = client.post(
        "/healthcare-services/",
        json={
            "name": "Cardiology",
        },
    )

    assert response.status_code == 401


# --------------------------------------------
# HEALTHCARE SERVICE AUTHORIZATION TEST
# --------------------------------------------

# AUTHORIZATION DENIED TEST
# --------------------------------------------
def test_list_healthcare_services_denies_organization_access(
    client,
    app,
    mocker,
):

    app.dependency_overrides[
        require_organization_access
    ] = mocker.Mock(
        side_effect=OrganizationAccessDeniedError()
    )

    try:
        response = client.get(
            "/healthcare-services/"
        )

        assert response.status_code == 403

    finally:
        app.dependency_overrides.pop(
            require_organization_access,
            None,
        )


def deny_organization_access():
    raise OrganizationAccessDeniedError()



# AUTHORIZATION ROUTER ACCESS TEST
# --------------------------------------------
def test_healthcare_service_router_declares_organization_access():
    routes = router.router.routes

    list_route = next(
        route
        for route in routes
        if route.path.endswith(
            "/healthcare-services/"
        )
        and "GET" in route.methods
    )

    dependency_names = {
        dependency.call.__name__
        for dependency in (
            list_route.dependant.dependencies
        )
    }

    assert (
        "require_organization_access"
        in dependency_names
    )