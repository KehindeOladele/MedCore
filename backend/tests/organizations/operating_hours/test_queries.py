from app.modules.organizations.operating_hours import queries
from tests.factories.constants import ORGANIZATION_ID, USER_ID


ENTRY_ID = "11111111-1111-1111-1111-111111111111"


def _query(mocker, data):
    query = mocker.Mock()
    for name in ("insert", "select", "eq", "is_", "limit", "order", "update"):
        getattr(query, name).return_value = query
    query.execute.return_value = mocker.Mock(data=data)
    return query


def test_create_inserts_data(mocker):
    query = _query(mocker, [{"id": ENTRY_ID}])
    supabase = mocker.patch.object(queries, "supabase")
    supabase.table.return_value = query
    result = queries.create_operating_hours({"organization_id": str(ORGANIZATION_ID)})
    assert result == {"id": ENTRY_ID}
    query.insert.assert_called_once()


def test_get_scopes_to_organization_and_excludes_deleted_rows(mocker):
    query = _query(mocker, [{"id": ENTRY_ID}])
    supabase = mocker.patch.object(queries, "supabase")
    supabase.table.return_value = query
    assert queries.get_operating_hours(ORGANIZATION_ID, ENTRY_ID) == {"id": ENTRY_ID}
    query.eq.assert_any_call("organization_id", str(ORGANIZATION_ID))
    query.is_.assert_called_once_with("deleted_at", "null")


def test_list_filters_a_day_and_orders_windows(mocker):
    query = _query(mocker, [])
    supabase = mocker.patch.object(queries, "supabase")
    supabase.table.return_value = query
    assert queries.list_operating_hours(ORGANIZATION_ID, day_of_week=2) == []
    query.eq.assert_any_call("day_of_week", 2)
    assert query.order.call_count == 2


def test_update_scopes_to_entry_and_organization(mocker):
    query = _query(mocker, [{"id": ENTRY_ID}])
    supabase = mocker.patch.object(queries, "supabase")
    supabase.table.return_value = query
    result = queries.update_operating_hours(ORGANIZATION_ID, ENTRY_ID, {"updated_by": str(USER_ID)})
    assert result["id"] == ENTRY_ID
    query.eq.assert_any_call("organization_id", str(ORGANIZATION_ID))
