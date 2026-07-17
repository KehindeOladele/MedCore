from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


# --------------------------------------
# GET ORGANIZATION PROFILE ROUTER TEST
# --------------------------------------
def test_get_profile_authenticated():

    response = client.get(
        "/organizations/profile",
        headers={
            "Authorization": "Bearer TEST_TOKEN"
        }
    )

    assert response.status_code == 200


# ----------------------------------------
# PATCH / UPDATE PROFILE ROUTER TEST
# ----------------------------------------
def test_update_profile():

    response = client.patch(
        "/organizations/profile",
        json={
            "name": "Updated Hospital"
        },
        headers={
            "Authorization": "Bearer TEST_TOKEN"
        }
    )

    assert response.status_code == 200

    assert (
        response.json()["name"]
        == "Updated Hospital"
    )

