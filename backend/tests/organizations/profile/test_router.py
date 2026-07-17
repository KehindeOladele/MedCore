from fastapi.testclient import TestClient
from main import app
from app.core.security import get_current_user


client = TestClient(app)


def override_current_user():
    return {
        "id": "user-123",
        "email": "admin@test.com",
    }

app.dependency_overrides[get_current_user] = override_current_user


# --------------------------------------
# GET ORGANIZATION PROFILE ROUTER TEST
# --------------------------------------
def test_get_profile_authenticated():

    response = response = client.get("/organizations/profile")

    assert response.status_code == 200


# ----------------------------------------
# PATCH / UPDATE PROFILE ROUTER TEST
# ----------------------------------------
def test_update_profile():

    response = client.patch("/organizations/profile")

    assert response.status_code == 200

    assert (
        response.json()["name"]
        == "Updated Hospital"
    )

