import pytest
from uuid import uuid4

from app.modules.organizations import dependencies
from app.modules.organizations.exceptions import (
    OrganizationAccessDeniedError,
    OrganizationNotFoundError,
)


# ---------------------------------------------------------
# Shared Test Data
# ---------------------------------------------------------

ORGANIZATION_ID = uuid4()
OTHER_ORGANIZATION_ID = uuid4()


@pytest.fixture
def organization():
    return {
        "id": str(ORGANIZATION_ID),
        "name": "Test Hospital",
        "type": "hospital",
        "active": True,
    }


@pytest.fixture
def current_user():
    return {
        "id": str(uuid4()),
        "email": "admin@test.com",
        "role": "admin",
        "organization_ids": [
            str(ORGANIZATION_ID),
        ],
    }


# ---------------------------------------------------------
# _user_has_organization_access()
# ---------------------------------------------------------

def test_user_has_organization_access_returns_true(
    current_user,
):
    result = dependencies._user_has_organization_access(
        current_user=current_user,
        organization_id=ORGANIZATION_ID,
    )

    assert result is True


def test_user_has_organization_access_returns_false_for_other_org(
    current_user,
):
    result = dependencies._user_has_organization_access(
        current_user=current_user,
        organization_id=OTHER_ORGANIZATION_ID,
    )

    assert result is False


def test_user_has_organization_access_supports_multiple_organizations():
    organization_one = uuid4()
    organization_two = uuid4()
    organization_three = uuid4()

    user = {
        "id": str(uuid4()),
        "organization_ids": [
            str(organization_one),
            str(organization_two),
        ],
    }

    assert dependencies._user_has_organization_access(
        user,
        organization_one,
    ) is True

    assert dependencies._user_has_organization_access(
        user,
        organization_two,
    ) is True

    assert dependencies._user_has_organization_access(
        user,
        organization_three,
    ) is False


def test_user_has_organization_access_handles_missing_organization_ids():
    user = {
        "id": str(uuid4()),
    }

    result = dependencies._user_has_organization_access(
        user,
        ORGANIZATION_ID,
    )

    assert result is False


def test_user_has_organization_access_handles_empty_organization_ids():
    user = {
        "id": str(uuid4()),
        "organization_ids": [],
    }

    result = dependencies._user_has_organization_access(
        user,
        ORGANIZATION_ID,
    )

    assert result is False


def test_user_has_organization_access_normalizes_uuid_types():
    user = {
        "id": str(uuid4()),
        "organization_ids": [
            str(ORGANIZATION_ID),
        ],
    }

    result = dependencies._user_has_organization_access(
        user,
        ORGANIZATION_ID,
    )

    assert result is True