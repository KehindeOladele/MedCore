from pytest_mock import MockerFixture


# ------------------------
# AUTH OVERRIDE
# ------------------------
def override_current_user():
    return {
        "id": "user-123",
        "email": "admin@test.com",
    }


# --------------------------------------
# GET PROFILE
# --------------------------------------
def test_get_profile_authenticated(
    authenticated_client,
    organization_profile_data,
    mocker: MockerFixture,
):
    mocker.patch(
        "app.modules.organizations.profile.router.get_user_organization_id",
        return_value="org1",
    )

    mocker.patch(
        "app.modules.organizations.profile.router.get_profile",
        return_value=organization_profile_data,
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
    updated_organization_profile_data,
    mocker: MockerFixture,
):
    mocker.patch(
        "app.modules.organizations.profile.router.get_user_organization_id",
        return_value="org1",
    )

    mocker.patch(
        "app.modules.organizations.profile.router.update_profile",
        return_value=updated_organization_profile_data,
    )

    response = authenticated_client.patch(
        "/organizations/profile",
        json={
            "name": "Updated Hospital"
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Hospital"