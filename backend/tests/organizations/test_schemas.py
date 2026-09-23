import pytest
from pydantic import ValidationError
from uuid import UUID, uuid4

from app.modules.organizations.schemas import (
    OrganizationBase,
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationLogo,
    RoleAssignment,
    OnboardingInvite,
    AcceptInviteRequest,
)

from tests.factories.organization import organization_row_factory
from tests.factories.constants import ORGANIZATION_ID, USER_ID


# ============================================================================
# ORGANIZATION BASE
# ============================================================================


def test_organization_base_accepts_factory_data():
    row = organization_row_factory()

    payload = OrganizationBase(
        name=row["name"],
        type=row["type"],
        email=row["email"],
        phone=row["phone"],
        address=row["address"],
        state=row["state"],
        country=row["country"],
    )

    assert payload.name == row["name"]
    assert payload.type == row["type"]
    assert payload.email == row["email"]
    assert payload.phone == row["phone"]
    assert payload.address == row["address"]
    assert payload.state == row["state"]
    assert payload.country == row["country"]


def test_organization_base_requires_name():
    with pytest.raises(ValidationError):
        OrganizationBase()


def test_organization_base_allows_optional_fields_to_be_omitted():
    payload = OrganizationBase(
        name="Test Hospital",
    )

    assert payload.name == "Test Hospital"
    assert payload.type is None
    assert payload.email is None
    assert payload.phone is None
    assert payload.address is None
    assert payload.state is None
    assert payload.country == "Nigeria"


def test_organization_base_defaults_country_to_nigeria():
    payload = OrganizationBase(
        name="Test Hospital",
    )

    assert payload.country == "Nigeria"


def test_organization_base_accepts_explicit_country():
    payload = OrganizationBase(
        name="Test Hospital",
        country="Ghana",
    )

    assert payload.country == "Ghana"


def test_organization_base_rejects_invalid_email():
    with pytest.raises(ValidationError):
        OrganizationBase(
            name="Test Hospital",
            email="invalid-email",
        )


def test_organization_base_accepts_valid_email():
    payload = OrganizationBase(
        name="Test Hospital",
        email="admin@example.com",
    )

    assert str(payload.email) == "admin@example.com"


# ============================================================================
# ORGANIZATION CREATE
# ============================================================================


def test_organization_create_accepts_valid_payload():
    row = organization_row_factory()

    payload = OrganizationCreate(
        name=row["name"],
        type=row["type"],
        email=row["email"],
        phone=row["phone"],
        address=row["address"],
        state=row["state"],
        country=row["country"],
        admin_email=row["email"],
        admin_password="SecurePassword123",
    )

    assert payload.name == row["name"]
    assert payload.type == row["type"]
    assert str(payload.email) == row["email"]
    assert payload.admin_email == row["email"]
    assert payload.admin_password == "SecurePassword123"
    assert payload.country == "Nigeria"


def test_organization_create_requires_admin_email():
    with pytest.raises(ValidationError):
        OrganizationCreate(
            name="Test Hospital",
            admin_password="SecurePassword123",
        )


def test_organization_create_requires_admin_password():
    with pytest.raises(ValidationError):
        OrganizationCreate(
            name="Test Hospital",
            admin_email="admin@example.com",
        )


def test_organization_create_rejects_invalid_admin_email():
    with pytest.raises(ValidationError):
        OrganizationCreate(
            name="Test Hospital",
            admin_email="invalid-email",
            admin_password="SecurePassword123",
        )


def test_organization_create_preserves_admin_password():
    payload = OrganizationCreate(
        name="Test Hospital",
        admin_email="admin@example.com",
        admin_password="SecurePassword123",
    )

    assert payload.admin_password == "SecurePassword123"


# ============================================================================
# ORGANIZATION UPDATE
# ============================================================================


def test_organization_update_accepts_partial_payload():
    payload = OrganizationUpdate(
        name="Updated Hospital",
    )

    assert payload.name == "Updated Hospital"


def test_organization_update_allows_empty_payload():
    payload = OrganizationUpdate()

    assert payload.model_dump(exclude_unset=True) == {}


def test_organization_update_accepts_all_supported_fields():
    payload = OrganizationUpdate(
        name="Updated Hospital",
        type="clinic",
        level="secondary",
        email="updated@example.com",
        phone="+2348012345678",
        address="456 New Street",
        state="Abuja",
        country="Nigeria",
    )

    assert payload.name == "Updated Hospital"
    assert payload.type == "clinic"
    assert payload.level == "secondary"
    assert str(payload.email) == "updated@example.com"
    assert payload.phone == "+2348012345678"
    assert payload.address == "456 New Street"
    assert payload.state == "Abuja"
    assert payload.country == "Nigeria"


def test_organization_update_rejects_invalid_email():
    with pytest.raises(ValidationError):
        OrganizationUpdate(
            email="invalid-email",
        )


def test_organization_update_accepts_explicit_none_values():
    payload = OrganizationUpdate(
        name=None,
        email=None,
        phone=None,
    )

    assert payload.name is None
    assert payload.email is None
    assert payload.phone is None


# ============================================================================
# ORGANIZATION LOGO
# ============================================================================


def test_organization_logo_accepts_valid_payload():
    organization_id = uuid4()

    payload = OrganizationLogo(
        id=organization_id,
        name="Test Hospital",
        type="hospital",
        email="admin@example.com",
        phone="+2348012345678",
        address="123 Main Street",
        state="Lagos",
        logo_url="https://example.com/logo.png",
    )

    assert payload.id == organization_id
    assert payload.name == "Test Hospital"
    assert payload.logo_url == "https://example.com/logo.png"


def test_organization_logo_requires_id():
    with pytest.raises(ValidationError):
        OrganizationLogo(
            name="Test Hospital",
        )


def test_organization_logo_rejects_invalid_uuid():
    with pytest.raises(ValidationError):
        OrganizationLogo(
            id="not-a-uuid",
            name="Test Hospital",
        )


def test_organization_logo_allows_null_logo_url():
    payload = OrganizationLogo(
        id=uuid4(),
        name="Test Hospital",
        logo_url=None,
    )

    assert payload.logo_url is None


# ============================================================================
# ROLE ASSIGNMENT
# ============================================================================


def test_role_assignment_accepts_valid_payload():
    user_id = uuid4()

    payload = RoleAssignment(
        user_id=user_id,
        role_name="org_admin",
        org_id=str(ORGANIZATION_ID),
    )

    assert payload.user_id == user_id
    assert payload.role_name == "org_admin"
    assert payload.org_id == str(ORGANIZATION_ID)


def test_role_assignment_requires_user_id():
    with pytest.raises(ValidationError):
        RoleAssignment(
            role_name="org_admin",
            org_id=str(ORGANIZATION_ID),
        )


def test_role_assignment_rejects_invalid_user_uuid():
    with pytest.raises(ValidationError):
        RoleAssignment(
            user_id="not-a-uuid",
            role_name="org_admin",
            org_id=str(ORGANIZATION_ID),
        )


def test_role_assignment_requires_role_name():
    with pytest.raises(ValidationError):
        RoleAssignment(
            user_id=USER_ID,
            org_id=str(ORGANIZATION_ID),
        )


def test_role_assignment_requires_org_id():
    with pytest.raises(ValidationError):
        RoleAssignment(
            user_id=USER_ID,
            role_name="org_admin",
        )


# ============================================================================
# ONBOARDING INVITE
# ============================================================================


def test_onboarding_invite_accepts_valid_payload():
    payload = OnboardingInvite(
        email="invite@example.com",
        role_name="org_admin",
        org_id=str(ORGANIZATION_ID),
    )

    assert str(payload.email) == "invite@example.com"
    assert payload.role_name == "org_admin"
    assert payload.org_id == str(ORGANIZATION_ID)


def test_onboarding_invite_rejects_invalid_email():
    with pytest.raises(ValidationError):
        OnboardingInvite(
            email="invalid-email",
            role_name="org_admin",
            org_id=str(ORGANIZATION_ID),
        )


def test_onboarding_invite_requires_email():
    with pytest.raises(ValidationError):
        OnboardingInvite(
            role_name="org_admin",
            org_id=str(ORGANIZATION_ID),
        )


def test_onboarding_invite_requires_role_name():
    with pytest.raises(ValidationError):
        OnboardingInvite(
            email="invite@example.com",
            org_id=str(ORGANIZATION_ID),
        )


def test_onboarding_invite_requires_org_id():
    with pytest.raises(ValidationError):
        OnboardingInvite(
            email="invite@example.com",
            role_name="org_admin",
        )


# ============================================================================
# ACCEPT INVITE REQUEST
# ============================================================================


def test_accept_invite_request_accepts_valid_payload():
    payload = AcceptInviteRequest(
        token="invite-token",
        password="SecurePassword123",
    )

    assert payload.token == "invite-token"
    assert payload.password == "SecurePassword123"


def test_accept_invite_request_requires_token():
    with pytest.raises(ValidationError):
        AcceptInviteRequest(
            password="SecurePassword123",
        )


def test_accept_invite_request_requires_password():
    with pytest.raises(ValidationError):
        AcceptInviteRequest(
            token="invite-token",
        )


def test_accept_invite_request_allows_empty_strings():
    payload = AcceptInviteRequest(
        token="",
        password="",
    )

    assert payload.token == ""
    assert payload.password == ""