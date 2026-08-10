import pytest
from uuid import uuid4

from app.modules.organizations import dependencies
from app.modules.organizations.exceptions import (
    OrganizationAccessDeniedError,
    OrganizationNotFoundError,
)
from tests.fixtures.auth import current_user
from tests.factories.organization import (
    ORGANIZATION_ID,
    OTHER_ORGANIZATION_ID
    )




# ---------------------------------------------------------
# USER ORGANIZATION ACCESS DEPENDENCY TEST
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
        "id": str(current_user),
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
        "id": str(current_user),
    }

    result = dependencies._user_has_organization_access(
        user,
        ORGANIZATION_ID,
    )

    assert result is False


def test_user_has_organization_access_handles_empty_organization_ids():
    user = {
        "id": str(current_user),
        "organization_ids": [],
    }

    result = dependencies._user_has_organization_access(
        user,
        ORGANIZATION_ID,
    )

    assert result is False


def test_user_has_organization_access_normalizes_uuid_types():
    user = {
        "id": str(current_user),
        "organization_ids": [
            str(ORGANIZATION_ID),
        ],
    }

    result = dependencies._user_has_organization_access(
        user,
        ORGANIZATION_ID,
    )

    assert result is True


# ---------------------------------------------------------
# REQUIRE ORGANIZATION MEMBER TEST
# ---------------------------------------------------------
def test_require_organization_member_success(
    mocker,
    current_user,
    organization,
):
    get_organization = mocker.patch.object(
        dependencies,
        "get_organization",
        return_value=organization,
    )

    result = dependencies.require_organization_member(
        organization_id=ORGANIZATION_ID,
        current_user=current_user,
    )

    assert result == organization

    get_organization.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
    )


def test_require_organization_member_raises_when_org_not_found(
    mocker,
    current_user,
):
    mocker.patch.object(
        dependencies,
        "get_organization",
        return_value=None,
    )

    with pytest.raises(
        OrganizationNotFoundError
    ):
        dependencies.require_organization_member(
            organization_id=ORGANIZATION_ID,
            current_user=current_user,
        )


def test_require_organization_member_raises_when_user_has_no_access(
    mocker,
    current_user,
    organization,
):
    mocker.patch.object(
        dependencies,
        "get_organization",
        return_value=organization,
    )

    current_user["organization_ids"] = [
        str(OTHER_ORGANIZATION_ID)
    ]

    with pytest.raises(
        OrganizationAccessDeniedError
    ):
        dependencies.require_organization_member(
            organization_id=ORGANIZATION_ID,
            current_user=current_user,
        )


# ---------------------------------------------------------
# REQUIRE ORGANIZATION ACCESS DEPENDENCY TEST
# ---------------------------------------------------------
def test_require_organization_access_returns_organization(
    organization,
):
    result = dependencies.require_organization_access(
        organization=organization,
    )

    assert result is organization