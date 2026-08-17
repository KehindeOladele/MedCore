import pytest

from app.modules.organizations.healthcare_services import router
from app.modules.organizations.healthcare_services.exceptions import (
    HealthcareServiceNotFoundError,
)

from app.modules.organizations.exceptions import (
    OrganizationAccessDeniedError,
)

from app.modules.organizations.dependencies import (
    require_organization_access,
    require_organization_admin,
)

from tests.factories.organization import (
    HEALTHCARE_SERVICE_ID,
    ORGANIZATION_ID,
)

from tests.factories.user import USER_ID


BASE_URL = (
    f"/organizations/{ORGANIZATION_ID}"
    "/healthcare-services"
)


# ---------------------------------------------------------
# CREATE HEALTHCARE SERVICE
# ---------------------------------------------------------


def test_create_healthcare_service_success(
    authenticated_client,
    mocker,
    healthcare_service_response,
):
    create_service = mocker.patch.object(
        router,
        "create_healthcare_service",
        return_value=healthcare_service_response,
    )

    response = authenticated_client.post(
        f"{BASE_URL}",
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


def test_create_healthcare_service_invalid_payload(
    authenticated_client,
):
    response = authenticated_client.post(
        f"{BASE_URL}",
        json={
            "name": "",
        },
    )

    assert response.status_code == 422


# ---------------------------------------------------------
# LIST HEALTHCARE SERVICES
# ---------------------------------------------------------


def test_list_healthcare_services_success(
    authenticated_client,
    mocker,
    healthcare_service_response,
):
    list_service = mocker.patch.object(
        router,
        "list_healthcare_services",
        return_value=[
            healthcare_service_response,
        ],
    )

    response = authenticated_client.get(
        f"{BASE_URL}"
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1
    assert body[0]["name"] == "Cardiology"

    list_service.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
    )


def test_list_healthcare_services_empty(
    authenticated_client,
    mocker,
):
    list_service = mocker.patch.object(
        router,
        "list_healthcare_services",
        return_value=[],
    )

    response = authenticated_client.get(
        f"{BASE_URL}"
    )

    assert response.status_code == 200
    assert response.json() == []

    list_service.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
    )


# ---------------------------------------------------------
# GET HEALTHCARE SERVICE
# ---------------------------------------------------------


def test_get_healthcare_service_success(
    authenticated_client,
    mocker,
    healthcare_service_response,
):
    get_service = mocker.patch.object(
        router,
        "get_healthcare_service",
        return_value=healthcare_service_response,
    )

    response = authenticated_client.get(
        f"{BASE_URL}/{HEALTHCARE_SERVICE_ID}"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["name"] == "Cardiology"

    get_service.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
        healthcare_service_id=HEALTHCARE_SERVICE_ID,
    )


def test_get_healthcare_service_not_found(
    authenticated_client,
    mocker,
):
    get_service = mocker.patch.object(
        router,
        "get_healthcare_service",
        side_effect=HealthcareServiceNotFoundError(),
    )

    response = authenticated_client.get(
        f"{BASE_URL}/{HEALTHCARE_SERVICE_ID}"
    )

    assert response.status_code == 404

    get_service.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
        healthcare_service_id=HEALTHCARE_SERVICE_ID,
    )


# ---------------------------------------------------------
# UPDATE HEALTHCARE SERVICE
# ---------------------------------------------------------


def test_update_healthcare_service_success(
    authenticated_client,
    mocker,
    healthcare_service_response,
):
    update_service = mocker.patch.object(
        router,
        "update_healthcare_service",
        return_value=healthcare_service_response,
    )

    response = authenticated_client.patch(
        f"{BASE_URL}/{HEALTHCARE_SERVICE_ID}",
        json={
            "name": "Updated Cardiology",
        },
    )

    assert response.status_code == 200

    body = response.json() 

    assert body["name"] == "Cardiology"

    update_service.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
        healthcare_service_id=HEALTHCARE_SERVICE_ID,
        payload=mocker.ANY,
        actor_id=USER_ID,
    )


# ---------------------------------------------------------
# DELETE HEALTHCARE SERVICE
# ---------------------------------------------------------


def test_delete_healthcare_service_success(
    authenticated_client,
    mocker,
):
    delete_service = mocker.patch.object(
        router,
        "delete_healthcare_service",
    )

    response = authenticated_client.delete(
        f"{BASE_URL}/{HEALTHCARE_SERVICE_ID}"
    )

    assert response.status_code == 204
    assert response.content == b""

    delete_service.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
        healthcare_service_id=HEALTHCARE_SERVICE_ID,
        actor_id=USER_ID,
    )


# ---------------------------------------------------------
# AUTHENTICATION
# ---------------------------------------------------------


@pytest.mark.parametrize(
    "method,path",
    [
        ("GET", f"{BASE_URL}"),
        (
            "GET",
            f"{BASE_URL}/{HEALTHCARE_SERVICE_ID}",
        ),
        ("POST", f"{BASE_URL}"),
        (
            "PATCH",
            f"{BASE_URL}/{HEALTHCARE_SERVICE_ID}",
        ),
        (
            "DELETE",
            f"{BASE_URL}/{HEALTHCARE_SERVICE_ID}",
        ),
    ],
)
def test_healthcare_service_routes_require_authentication(
    client,
    method,
    path,
):
    response = client.request(
        method,
        path,
    )

    assert response.status_code == 401


# ---------------------------------------------------------
# READ AUTHORIZATION
# ---------------------------------------------------------


def test_list_healthcare_services_denies_organization_access(
    authenticated_client,
    mocker,
):
    app = authenticated_client.app

    def deny_organization_access():
        raise OrganizationAccessDeniedError()

    app.dependency_overrides[
        require_organization_access
    ] = deny_organization_access

    try:
        response = authenticated_client.get(
            f"{BASE_URL}"
        )

        assert response.status_code == 403

    finally:
        app.dependency_overrides.pop(
            require_organization_access,
            None,
        )


def test_get_healthcare_service_denies_organization_access( 
        authenticated_client, 
        mocker, 
): 
    app = authenticated_client.app 

    def deny_organization_access():
        raise OrganizationAccessDeniedError()

    app.dependency_overrides[ 
        require_organization_access 
        ] = deny_organization_access

    try: 
        response = authenticated_client.get( 
            f"{BASE_URL}/{HEALTHCARE_SERVICE_ID}" 
            ) 

        assert response.status_code == 403 

    finally: 
        app.dependency_overrides.pop( 
            require_organization_access, 
            None, 
            )

# --------------------------------------------------------- 
# MUTATION AUTHORIZATION 
# --------------------------------------------------------- 
@pytest.mark.parametrize( 
    "method,path,payload", 
    [ 
        ( 
            "POST", 
            f"{BASE_URL}", 
            { 
                "name": "Cardiology", 
                "description": "Cardiology services", 
                }, 
            ), 
            ( 
                "PATCH", f"{BASE_URL}/{HEALTHCARE_SERVICE_ID}", 
                { "name": "Updated Cardiology", }, 
                ), 
                ( 
                    "DELETE", f"{BASE_URL}/{HEALTHCARE_SERVICE_ID}", 
                    None, 
                ), 
    ], 
    ) 

def test_healthcare_service_mutations_require_admin( 
    authenticated_client, 
    mocker, 
    method, 
    path, 
    payload, 
    ): 

    app = authenticated_client.app 

    def deny_organization_access():
        raise OrganizationAccessDeniedError()

    app.dependency_overrides[ 
        require_organization_access 
        ] = deny_organization_access

    try: 
        response = authenticated_client.request( 
            method, 
            path, json=payload, 
            ) 

        assert response.status_code == 403 

    finally: app.dependency_overrides.pop( 
        require_organization_admin, 
        None, 
        )        


# ---------------------------------------------------------
# ROUTER DEPENDENCY DECLARATION
# ---------------------------------------------------------
def test_healthcare_service_list_declares_organization_access():
    routes = router.router.routes

    list_route = next(
        route
        for route in routes
        if route.path == "/{organization_id}/healthcare-services"
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