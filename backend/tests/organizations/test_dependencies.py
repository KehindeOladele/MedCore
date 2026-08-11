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
    OTHER_ORGANIZATION_ID,
    organization_factory
    )




# ---------------------------------------------------------
# USER ORGANIZATION ACCESS DEPENDENCY TEST
# ---------------------------------------------------------
def test_user_has_organization_access_returns_true():
    current_user = {
        "id": str(uuid4()),
        "organization_ids": [
            str(ORGANIZATION_ID),
        ],
    }

    result = dependencies._user_has_organization_access(
        current_user=current_user,
        organization_id=ORGANIZATION_ID,
    )

    assert result is True


def test_user_has_organization_access_returns_false_for_other_organization():
    current_user = {
        "id": str(uuid4()),
        "organization_ids": [
            str(ORGANIZATION_ID),
        ],
    }

    result = dependencies._user_has_organization_access(
        current_user=current_user,
        organization_id=OTHER_ORGANIZATION_ID,
    )

    assert result is False


def test_user_has_organization_access_supports_multiple_organizations():
    organization_one = uuid4()
    organization_two = uuid4()
    organization_three = uuid4()

    current_user = {
        "id": str(uuid4()),
        "organization_ids": [
            str(organization_one),
            str(organization_two),
        ],
    }

    assert dependencies._user_has_organization_access(
        current_user=current_user,
        organization_id=organization_one,
    ) is True

    assert dependencies._user_has_organization_access(
        current_user=current_user,
        organization_id=organization_two,
    ) is True

    assert dependencies._user_has_organization_access(
        current_user=current_user,
        organization_id=organization_three,
    ) is False


def test_user_has_organization_access_returns_false_when_organization_ids_missing():
    current_user = {
        "id": str(uuid4()),
    }

    result = dependencies._user_has_organization_access(
        current_user=current_user,
        organization_id=ORGANIZATION_ID,
    )

    assert result is False


def test_user_has_organization_access_returns_false_when_organization_ids_empty():
    current_user = {
        "id": str(uuid4()),
        "organization_ids": [],
    }

    result = dependencies._user_has_organization_access(
        current_user=current_user,
        organization_id=ORGANIZATION_ID,
    )

    assert result is False


def test_user_has_organization_access_normalizes_uuid_values():
    current_user = {
        "id": str(uuid4()),
        "organization_ids": [
            ORGANIZATION_ID,
        ],
    }

    result = dependencies._user_has_organization_access(
        current_user=current_user,
        organization_id=ORGANIZATION_ID,
    )

    assert result is True


# ---------------------------------------------------------
# REQUIRE ORGANIZATION ACCESS DEPENDENCY TEST
# ---------------------------------------------------------
def test_require_organization_access_returns_organization(
    organization= organization_factory,
):
    result = dependencies.require_organization_access(
        organization=organization,
    )

    assert result is organization