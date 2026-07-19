from unittest.mock import patch

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
@patch("app.modules.organizations.profile.router.get_profile")
@patch("app.modules.organizations.profile.router.get_user_organization_id")
def test_get_profile_authenticated(
    mock_get_org,
    mock_get_profile,
):
    mock_get_org.return_value = "org1"
    mock_get_profile.return_value = PROFILE_RESPONSE

    response = client.get("/organizations/profile")

    assert response.status_code == 200
    assert response.json()["id"] == "org1"

    mock_get_org.assert_called_once_with("user-123")
    mock_get_profile.assert_called_once_with("org1")


# --------------------------------------
# UPDATE PROFILE
# --------------------------------------
@patch("app.modules.organizations.profile.router.update_profile")
@patch("app.modules.organizations.profile.router.get_user_organization_id")
def test_update_profile(
    mock_get_org,
    mock_update_profile,
):
    mock_get_org.return_value = "org1"

    updated = PROFILE_RESPONSE.copy()
    updated["name"] = "Updated Hospital"

    mock_update_profile.return_value = updated

    response = client.patch(
        "/organizations/profile",
        json={
            "name": "Updated Hospital"
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Hospital"

    mock_get_org.assert_called_once_with("user-123")
    mock_update_profile.assert_called_once()