from app.modules.organizations.branding import queries
from tests.factories.constants import ORGANIZATION_ID


def _query(mocker, data):
    query = mocker.Mock()
    for name in ("select", "eq", "update", "maybe_single"):
        getattr(query, name).return_value = query
    query.execute.return_value = mocker.Mock(data=data)
    return query


def test_get_branding_selects_the_organization_record(mocker):
    query = _query(mocker, {"id": str(ORGANIZATION_ID)})
    admin = mocker.patch.object(queries, "supabase_admin")
    admin.table.return_value = query
    assert queries.get_branding(ORGANIZATION_ID)["id"] == str(ORGANIZATION_ID)
    query.eq.assert_called_once_with("id", str(ORGANIZATION_ID))


def test_update_branding_limits_write_to_organization(mocker):
    query = _query(mocker, {"id": str(ORGANIZATION_ID), "primary_color": "#123456"})
    admin = mocker.patch.object(queries, "supabase_admin")
    admin.table.return_value = query
    result = queries.update_branding(ORGANIZATION_ID, {"primary_color": "#123456"})
    assert result["primary_color"] == "#123456"
    query.update.assert_called_once_with({"primary_color": "#123456"})
    query.eq.assert_called_once_with("id", str(ORGANIZATION_ID))
