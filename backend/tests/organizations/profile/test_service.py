import pytest
from unittest.mock import patch
from app.modules.organizations.profile.service import (
    get_profile,
    update_profile
)
from app.modules.organizations.exceptions import (
    OrganizationNotFoundError,
)
from app.modules.organizations.profile.schemas import (
    OrganizationProfileUpdate,
)
from tests.conftest import organization_data


# ------------------
# GET PROFILE TESTS
# ------------------
@patch(
    "app.modules.organizations.profile.service.get_organization_profile"
)
def test_get_profile(mock_get):

    mock_get.return_value = {
        "id": "org1",
        "name": "MedCore",
        "active": True,
        "type": "Hospital",
    }

    profile = get_profile("org1")

    assert profile.name == "MedCore"


# ---------------------------------
# GET ORGANIZATION NOT FOUND TESTS
# ---------------------------------
@patch(
    "app.modules.organizations.profile.service.get_organization_profile"
)
def test_get_profile_not_found(mock_get):

    mock_get.return_value = None

    with pytest.raises(
        OrganizationNotFoundError
    ):
        get_profile("missing")


# ---------------------
# UPDATE PROFILE TESTS
# ---------------------
@patch(
    "app.modules.organizations.profile.service.log_audit_event"
)
@patch(
    "app.modules.organizations.profile.service.update_organization_profile"
)
@patch(
    "app.modules.organizations.profile.service.get_organization_profile"
)
def test_update_profile(
    mock_get,
    mock_update,
    mock_audit,
    organization_data,
):

    updated_org = organization_data.copy()
    updated_org["name"] = "New Name"

    mock_get.return_value = organization_data
    mock_update.return_value = updated_org

    payload = OrganizationProfileUpdate(
        name="New Name"
    )

    result = update_profile(
        "org1",
        payload,
        actor_id="user1",
    )

    mock_update.assert_called_once()

    args = mock_update.call_args.args

    assert args[0] == "org1"
    assert args[1]["name"] == "New Name"
    assert "updated_at" in args[1]

    mock_audit.assert_called_once()