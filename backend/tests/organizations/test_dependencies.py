import pytest
from uuid import uuid4, UUID
from tests.factories.user import user_factory
from app.modules.organizations import dependencies
from app.modules.organizations.exceptions import (
    OrganizationAccessDeniedError,
    OrganizationNotFoundError,
)
from tests.factories.organization import (
    ORGANIZATION_ID,
    OTHER_ORGANIZATION_ID
    )




# ---------------------------------------------------------
# USER ORGANIZATION ACCESS DEPENDENCY TEST
# ---------------------------------------------------------
def test_user_has_organization_access_matching_organization():
    organization_id = ORGANIZATION_ID

    current_user = user_factory

    assert dependencies._user_has_organization_access(
        current_user=current_user,
        organization_id=organization_id,
    ) is True


def test_user_has_organization_access_wrong_organization():
    organization_id = ORGANIZATION_ID
    other_organization_id = OTHER_ORGANIZATION_ID

    current_user = {
        "id": "user1",
        "organization_ids": [
            str(organization_id),
        ],
    }

    assert dependencies._user_has_organization_access(
        current_user=current_user,
        organization_id=other_organization_id,
    ) is False


def test_user_has_organization_access_multiple_organizations():
    organization_id = ORGANIZATION_ID
    other_organization_id = uuid4()

    current_user = {
        "id": "user1",
        "organization_ids": [
            str(organization_id),
            str(other_organization_id),
        ],
    }

    assert dependencies._user_has_organization_access(
        current_user=current_user,
        organization_id=other_organization_id,
    ) is True


def test_user_has_organization_access_missing_organization_ids():
    current_user = {
        "id": "user1",
    }

    assert dependencies._user_has_organization_access(
        current_user=current_user,
        organization_id=uuid4(),
    ) is False


def test_user_has_organization_access_empty_organization_ids():
    current_user = {
        "id": "user1",
        "organization_ids": [],
    }

    assert dependencies._user_has_organization_access(
        current_user=current_user,
        organization_id=uuid4(),
    ) is False


def test_user_has_organization_access_normalizes_uuid_values():
    organization_id = uuid4()

    current_user = {
        "id": "user1",
        "organization_ids": [
            organization_id,
        ],
    }

    assert dependencies._user_has_organization_access(
        current_user=current_user,
        organization_id=UUID(str(organization_id)),
    ) is True


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


# ---------------------------------------------------------
# REQUIRE ORGANIZATION MEMBER TEST
# ---------------------------------------------------------

# ORGANIZATION MEMBER SUCCESS TEST
# ---------------------------------------------------------
def test_require_organization_member_success(
    mocker,
):
    organization_id = ORGANIZATION_ID

    organization = {
        "id": str(organization_id),
        "name": "Test Hospital",
        "active": True,
    }

    current_user = {
        "id": "user1",
        "organization_ids": [
            str(organization_id),
        ],
    }

    mocker.patch.object(
        dependencies,
        "get_organization",
        return_value=organization,
    )

    result = dependencies.require_organization_member(
        organization_id=organization_id,
        current_user=current_user,
    )

    assert result is organization



# ORGANIZATION MEMBER NOT FOUND TEST
# ---------------------------------------------------------
def test_require_organization_member_organization_not_found(
    mocker,
):
    organization_id = uuid4()

    mocker.patch.object(
        dependencies,
        "get_organization",
        return_value=None,
    )

    current_user = {
        "id": "user1",
        "organization_ids": [
            str(organization_id),
        ],
    }

    with pytest.raises(
        OrganizationNotFoundError
    ):
        dependencies.require_organization_member(
            organization_id=organization_id,
            current_user=current_user,
        )


# ORGANIZATION MEMBER DENIED TEST
# ---------------------------------------------------------
def test_require_organization_member_access_denied(
    mocker,
):
    organization_id = uuid4()

    organization = {
        "id": str(organization_id),
        "name": "Test Hospital",
        "active": True,
    }

    mocker.patch.object(
        dependencies,
        "get_organization",
        return_value=organization,
    )

    current_user = {
        "id": "user1",
        "organization_ids": [],
    }

    with pytest.raises(
        OrganizationAccessDeniedError
    ):
        dependencies.require_organization_member(
            organization_id=organization_id,
            current_user=current_user,
        )