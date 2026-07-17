from unittest.mock import MagicMock, patch

from app.modules.organizations.profile.queries import (
    get_organization_profile,
)


@patch("app.modules.organizations.profile.queries.supabase_admin")
def test_get_profile(mock_supabase):

    mock_response = MagicMock()
    mock_response.data = {
        "id": "org-123",
        "name": "MedCore"
    }

    (
        mock_supabase
        .table.return_value
        .select.return_value
        .eq.return_value
        .maybe_single.return_value
        .execute.return_value
    ) = mock_response

    organization = get_organization_profile("org-123")

    assert organization["name"] == "MedCore"