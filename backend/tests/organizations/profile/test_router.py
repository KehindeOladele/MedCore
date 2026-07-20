from pytest_mock import MockerFixture

from fastapi.testclient import TestClient

from main import app
from app.core.security import get_current_user


# ------------------------
# TEST CLIENT
# ------------------------
client = TestClient(app)


# ------------------------
# AUTH OVERRIDE
# ------------------------
def override_current_user():
    return {
        "id": "user-123",
        "email": "admin@test.com",
    }


app.dependency_overrides[get_current_user] = override_current_user


# ------------------------
# SHARED MOCK PROFILE
# ------------------------
PROFILE_RESPONSE = {
    "id": "org1",
    "active": True,
    "name": "Test Hospital",
    "type": "hospital",
    "telecom": {
        "phone": "08012345678",
        "email": "admin@test.com",
        "website": "https://hospital.test",
    },
    "address": {
        "line": "123 Main Street",
        "city": "Lagos",
        "state": "Lagos",
        "postal_code": "100001",
        "country": "Nigeria",
    },
    "description": None,
    "logo_url": None,
    "timezone": "Africa/Lagos",
    "setup_completed": False,
}


# --------------------------------------
# GET PROFILE
# --------------------------------------
def test_get_profile_authenticated(
    authenticated_client,
    organization_data,
    mocker: MockerFixture,
):
    mocker.patch(
        "app.modules.organizations.profile.router.get_user_organization_id",
        return_value="org1",
    )

    mocker.patch(
        "app.modules.organizations.profile.router.get_profile",
        return_value=organization_data,
    )

    response = authenticated_client.get(
        "/organizations/profile"
    )

    assert response.status_code == 200
    assert response.json()["id"] == "org1"


# --------------------------------------
# UPDATE PROFILE
# --------------------------------------
def test_update_profile(
    authenticated_client,
    updated_organization_data,
    mocker: MockerFixture,
):
    mocker.patch(
        "app.modules.organizations.profile.router.get_user_organization_id",
        return_value="org1",
    )

    mocker.patch(
        "app.modules.organizations.profile.router.update_profile",
        return_value=updated_organization_data,
    )

    response = authenticated_client.patch(
        "/organizations/profile",
        json={
            "name": "Updated Hospital"
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Hospital"