from app.modules.organizations.operating_hours import queries

from tests.factories.constants import ORGANIZATION_ID, USER_ID


ENTRY_ID = "11111111-1111-1111-1111-111111111111"


def _query(mocker, data):
    query = mocker.Mock()

    for name in (
        "insert",
        "select",
        "eq",
        "is_",
        "limit",
        "order",
        "update",
    ):
        getattr(query, name).return_value = query

    query.execute.return_value = mocker.Mock(data=data)

    return query


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------


def test_create_operating_hours_inserts_into_table_and_returns_first_row(mocker):
    row = {
        "id": ENTRY_ID,
        "organization_id": str(ORGANIZATION_ID),
    }

    query = _query(mocker, [row])

    supabase = mocker.patch.object(queries, "supabase")
    supabase.table.return_value = query

    payload = {
        "organization_id": str(ORGANIZATION_ID),
        "day_of_week": 0,
        "slot_index": 0,
        "opens_at": "08:00:00",
        "closes_at": "16:00:00",
        "is_closed": False,
        "created_by": str(USER_ID),
        "updated_by": str(USER_ID),
    }

    result = queries.create_operating_hours(payload)

    assert result == row

    supabase.table.assert_called_once_with(queries.TABLE)
    query.insert.assert_called_once_with(payload)
    query.execute.assert_called_once()


# ---------------------------------------------------------------------------
# Get
# ---------------------------------------------------------------------------


def test_get_operating_hours_scopes_to_organization_and_entry(mocker):
    row = {"id": ENTRY_ID}

    query = _query(mocker, [row])

    supabase = mocker.patch.object(queries, "supabase")
    supabase.table.return_value = query

    result = queries.get_operating_hours(
        ORGANIZATION_ID,
        ENTRY_ID,
    )

    assert result == row

    supabase.table.assert_called_once_with(queries.TABLE)

    query.eq.assert_any_call(
        "organization_id",
        str(ORGANIZATION_ID),
    )
    query.eq.assert_any_call(
        "id",
        str(ENTRY_ID),
    )


def test_get_operating_hours_excludes_soft_deleted_rows(mocker):
    query = _query(mocker, [{"id": ENTRY_ID}])

    supabase = mocker.patch.object(queries, "supabase")
    supabase.table.return_value = query

    queries.get_operating_hours(
        ORGANIZATION_ID,
        ENTRY_ID,
    )

    query.is_.assert_called_once_with(
        "deleted_at",
        "null",
    )


def test_get_operating_hours_limits_to_one_row(mocker):
    query = _query(mocker, [{"id": ENTRY_ID}])

    supabase = mocker.patch.object(queries, "supabase")
    supabase.table.return_value = query

    queries.get_operating_hours(
        ORGANIZATION_ID,
        ENTRY_ID,
    )

    query.limit.assert_called_once_with(1)


def test_get_operating_hours_returns_none_when_no_row_exists(mocker):
    query = _query(mocker, [])

    supabase = mocker.patch.object(queries, "supabase")
    supabase.table.return_value = query

    result = queries.get_operating_hours(
        ORGANIZATION_ID,
        ENTRY_ID,
    )

    assert result is None


# ---------------------------------------------------------------------------
# List
# ---------------------------------------------------------------------------


def test_list_operating_hours_scopes_to_organization(mocker):
    query = _query(mocker, [])

    supabase = mocker.patch.object(queries, "supabase")
    supabase.table.return_value = query

    result = queries.list_operating_hours(ORGANIZATION_ID)

    assert result == []

    query.eq.assert_any_call(
        "organization_id",
        str(ORGANIZATION_ID),
    )


def test_list_operating_hours_excludes_soft_deleted_rows(mocker):
    query = _query(mocker, [])

    supabase = mocker.patch.object(queries, "supabase")
    supabase.table.return_value = query

    queries.list_operating_hours(ORGANIZATION_ID)

    query.is_.assert_called_once_with(
        "deleted_at",
        "null",
    )


def test_list_operating_hours_orders_by_day_then_slot(mocker):
    query = _query(mocker, [])

    supabase = mocker.patch.object(queries, "supabase")
    supabase.table.return_value = query

    queries.list_operating_hours(ORGANIZATION_ID)

    assert query.order.call_count == 2

    query.order.assert_any_call("day_of_week")
    query.order.assert_any_call("slot_index")


def test_list_operating_hours_filters_by_day_when_requested(mocker):
    query = _query(mocker, [])

    supabase = mocker.patch.object(queries, "supabase")
    supabase.table.return_value = query

    result = queries.list_operating_hours(
        ORGANIZATION_ID,
        day_of_week=2,
    )

    assert result == []

    query.eq.assert_any_call(
        "day_of_week",
        2,
    )


def test_list_operating_hours_does_not_add_day_filter_when_not_requested(mocker):
    query = _query(mocker, [])

    supabase = mocker.patch.object(queries, "supabase")
    supabase.table.return_value = query

    queries.list_operating_hours(ORGANIZATION_ID)

    day_filter_calls = [
        call
        for call in query.eq.call_args_list
        if call.args[0] == "day_of_week"
    ]

    assert day_filter_calls == []


def test_list_operating_hours_returns_all_rows(mocker):
    rows = [
        {"id": "1", "day_of_week": 0, "slot_index": 0},
        {"id": "2", "day_of_week": 0, "slot_index": 1},
        {"id": "3", "day_of_week": 1, "slot_index": 0},
    ]

    query = _query(mocker, rows)

    supabase = mocker.patch.object(queries, "supabase")
    supabase.table.return_value = query

    result = queries.list_operating_hours(ORGANIZATION_ID)

    assert result == rows


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------


def test_update_operating_hours_scopes_to_organization_and_entry(mocker):
    row = {"id": ENTRY_ID}

    query = _query(mocker, [row])

    supabase = mocker.patch.object(queries, "supabase")
    supabase.table.return_value = query

    payload = {
        "closes_at": "18:00:00",
        "updated_by": str(USER_ID),
    }

    result = queries.update_operating_hours(
        ORGANIZATION_ID,
        ENTRY_ID,
        payload,
    )

    assert result == row

    supabase.table.assert_called_once_with(queries.TABLE)

    query.update.assert_called_once_with(payload)

    query.eq.assert_any_call(
        "organization_id",
        str(ORGANIZATION_ID),
    )
    query.eq.assert_any_call(
        "id",
        str(ENTRY_ID),
    )


def test_update_operating_hours_returns_first_updated_row(mocker):
    row = {
        "id": ENTRY_ID,
        "updated_by": str(USER_ID),
    }

    query = _query(mocker, [row])

    supabase = mocker.patch.object(queries, "supabase")
    supabase.table.return_value = query

    result = queries.update_operating_hours(
        ORGANIZATION_ID,
        ENTRY_ID,
        {"updated_by": str(USER_ID)},
    )

    assert result["id"] == ENTRY_ID
    assert result["updated_by"] == str(USER_ID)


# ---------------------------------------------------------------------------
# Soft delete
# ---------------------------------------------------------------------------


def test_soft_delete_operating_hours_delegates_to_update(mocker):
    updated_row = {
        "id": ENTRY_ID,
        "deleted_at": "2026-08-21T10:00:00+00:00",
        "updated_by": str(USER_ID),
    }

    update = mocker.patch.object(
        queries,
        "update_operating_hours",
        return_value=updated_row,
    )

    data = {
        "deleted_at": "2026-08-21T10:00:00+00:00",
        "updated_at": "2026-08-21T10:00:00+00:00",
        "updated_by": str(USER_ID),
    }

    result = queries.soft_delete_operating_hours(
        ORGANIZATION_ID,
        ENTRY_ID,
        data,
    )

    assert result == updated_row

    update.assert_called_once_with(
        ORGANIZATION_ID,
        ENTRY_ID,
        data,
    )