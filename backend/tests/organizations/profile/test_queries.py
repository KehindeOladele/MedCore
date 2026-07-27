# tests/organizations/profile/test_queries.py
from app.modules.organizations.profile.queries import (
    get_organization_profile,
    update_organization_profile,
)
from tests.helpers.responses import mock_list, mock_single
from tests.helpers.supabase import patch_supabase_table

ORGANIZATION_PROFILE = {
    "id": "org1",
    "name": "MedCore",
    "active": True,
    "type": "Hospital",
    "phone": "+2348000000000",
    "email": "admin@test.com",
    "website": "https://medcore.com",
    "address": "1 Health Avenue",
    "city": "Lagos",
    "state": "Lagos",
    "postal_code": "100001",
    "country": "Nigeria",
    "description": None,
    "logo_url": None,
    "timezone": "Africa/Lagos",
    "setup_completed": False,
}


def test_get_organization_profile_returns_profile(mocker):
    supabase_admin, chain = patch_supabase_table(
        mocker,
        "app.modules.organizations.profile.queries.supabase_admin",
        response=mock_single(ORGANIZATION_PROFILE),
    )

    result = get_organization_profile("org1")

    assert result == ORGANIZATION_PROFILE
    supabase_admin.table.assert_called_once_with("organizations")
    chain.select.assert_called_once_with("*")
    chain.eq.assert_called_once_with("id", "org1")
    chain.maybe_single.assert_called_once()
    chain.execute.assert_called_once()


def test_get_organization_profile_returns_none_when_missing(mocker):
    supabase_admin, chain = patch_supabase_table(
        mocker,
        "app.modules.organizations.profile.queries.supabase_admin",
        response=mock_single(None),
    )

    result = get_organization_profile("missing-org")

    assert result is None
    supabase_admin.table.assert_called_once_with("organizations")
    chain.select.assert_called_once_with("*")
    chain.eq.assert_called_once_with("id", "missing-org")
    chain.maybe_single.assert_called_once()
    chain.execute.assert_called_once()


def test_update_organization_profile_returns_updated_record(mocker):
    updated_profile = {**ORGANIZATION_PROFILE, "name": "Updated Hospital"}

    supabase_admin, chain = patch_supabase_table(
        mocker,
        "app.modules.organizations.profile.queries.supabase_admin",
        response=mock_list([updated_profile]),
    )

    result = update_organization_profile(
        "org1",
        {"name": "Updated Hospital"},
    )

    assert result == updated_profile
    supabase_admin.table.assert_called_once_with("organizations")
    chain.update.assert_called_once_with({"name": "Updated Hospital"})
    chain.eq.assert_called_once_with("id", "org1")
    chain.execute.assert_called_once()


def test_update_organization_profile_returns_none_when_missing(mocker):
    supabase_admin, chain = patch_supabase_table(
        mocker,
        "app.modules.organizations.profile.queries.supabase_admin",
        response=mock_empty(),
    )

    result = update_organization_profile(
        "missing-org",
        {"name": "Updated Hospital"},
    )

    assert result is None
    supabase_admin.table.assert_called_once_with("organizations")
    chain.update.assert_called_once_with({"name": "Updated Hospital"})
    chain.eq.assert_called_once_with("id", "missing-org")
    chain.execute.assert_called_once()