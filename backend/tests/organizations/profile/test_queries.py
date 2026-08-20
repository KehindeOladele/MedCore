# tests/test_queries.py
from app.modules.organizations.profile.queries import get_organization_profile
from tests.helpers.responses import mock_single
from tests.helpers.supabase import patch_supabase_table


def test_get_profile(mocker):
    supabase_admin, chain = patch_supabase_table(
        mocker,
        "app.modules.organizations.profile.queries.supabase_admin",
        response=mock_single(
            {
                "id": "org-123",
                "name": "MedCore",
            }
        ),
    )

    organization = get_organization_profile("org-123")

    assert organization["name"] == "MedCore"

    supabase_admin.table.assert_called_once_with("organizations")
    chain.select.assert_called_once_with("*")
    chain.eq.assert_called_once_with("id", "org-123")
    chain.maybe_single.assert_called_once()
    chain.execute.assert_called_once()