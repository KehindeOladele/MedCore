from uuid import UUID
from tests.factories.constants import ORGANIZATION_ID
from app.modules.organizations.branding import queries


ORGANIZATION_ID = ORGANIZATION_ID


BRANDING_DATA = {
    "id": str(ORGANIZATION_ID),
    "logo_url": "https://storage.example.com/logo.png",
    "logo_path": f"{ORGANIZATION_ID}/logo.png",
    "primary_color": "#FFFFFF",
    "secondary_color": "#000000",
}


# ====================================================================================
# GET BRANDING
# ====================================================================================


def test_get_branding_returns_branding_record(mocker):
    execute = mocker.Mock(
        return_value=mocker.Mock(
            data=BRANDING_DATA
        )
    )

    query = mocker.Mock()
    query.select.return_value = query
    query.eq.return_value = query
    query.maybe_single.return_value = query
    query.execute = execute

    supabase = mocker.patch.object(
        queries,
        "supabase_admin",
    )

    supabase.table.return_value = query

    result = queries.get_branding(
        organization_id=ORGANIZATION_ID,
    )

    assert result == BRANDING_DATA

    supabase.table.assert_called_once_with(
        "organizations",
    )

    query.select.assert_called_once_with(
        "id, logo_url, logo_path, primary_color, secondary_color",
    )

    query.eq.assert_called_once_with(
        "id",
        str(ORGANIZATION_ID),
    )

    query.maybe_single.assert_called_once_with()

    execute.assert_called_once_with()


def test_get_branding_returns_none_when_record_not_found(mocker):
    execute = mocker.Mock(
        return_value=mocker.Mock(
            data=None
        )
    )

    query = mocker.Mock()
    query.select.return_value = query
    query.eq.return_value = query
    query.maybe_single.return_value = query
    query.execute = execute

    supabase = mocker.patch.object(
        queries,
        "supabase_admin",
    )

    supabase.table.return_value = query

    result = queries.get_branding(
        organization_id=ORGANIZATION_ID,
    )

    assert result is None

    supabase.table.assert_called_once_with(
        "organizations",
    )

    query.eq.assert_called_once_with(
        "id",
        str(ORGANIZATION_ID),
    )

    query.maybe_single.assert_called_once_with()
    execute.assert_called_once_with()


def test_get_branding_returns_none_when_response_data_is_falsy(mocker):
    execute = mocker.Mock(
        return_value=mocker.Mock(
            data={}
        )
    )

    query = mocker.Mock()
    query.select.return_value = query
    query.eq.return_value = query
    query.maybe_single.return_value = query
    query.execute = execute

    supabase = mocker.patch.object(
        queries,
        "supabase_admin",
    )

    supabase.table.return_value = query

    result = queries.get_branding(
        organization_id=ORGANIZATION_ID,
    )

    assert result is None


# ====================================================================================
# UPDATE BRANDING
# ====================================================================================


def test_update_branding_returns_updated_record(mocker):
    updates = {
        "primary_color": "#FF0000",
        "secondary_color": "#00FF00",
    }

    updated_data = {
        **BRANDING_DATA,
        **updates,
    }

    execute = mocker.Mock(
        return_value=mocker.Mock(
            data=updated_data
        )
    )

    query = mocker.Mock()
    query.update.return_value = query
    query.eq.return_value = query
    query.select.return_value = query
    query.maybe_single.return_value = query
    query.execute = execute

    supabase = mocker.patch.object(
        queries,
        "supabase_admin",
    )

    supabase.table.return_value = query

    result = queries.update_branding(
        organization_id=ORGANIZATION_ID,
        updates=updates,
    )

    assert result == updated_data

    supabase.table.assert_called_once_with(
        "organizations",
    )

    query.update.assert_called_once_with(
        updates,
    )

    query.eq.assert_called_once_with(
        "id",
        str(ORGANIZATION_ID),
    )

    query.select.assert_called_once_with(
        "id, logo_url, logo_path, primary_color, secondary_color",
    )

    query.maybe_single.assert_called_once_with()

    execute.assert_called_once_with()


def test_update_branding_preserves_update_payload(mocker):
    updates = {
        "logo_path": f"{ORGANIZATION_ID}/logo.webp",
        "logo_url": "https://storage.example.com/logo.webp",
        "updated_at": "2026-08-23T12:00:00+00:00",
    }

    execute = mocker.Mock(
        return_value=mocker.Mock(
            data=BRANDING_DATA,
        )
    )

    query = mocker.Mock()
    query.update.return_value = query
    query.eq.return_value = query
    query.select.return_value = query
    query.maybe_single.return_value = query
    query.execute = execute

    supabase = mocker.patch.object(
        queries,
        "supabase_admin",
    )

    supabase.table.return_value = query

    queries.update_branding(
        organization_id=ORGANIZATION_ID,
        updates=updates,
    )

    query.update.assert_called_once_with(
        updates,
    )

    # Ensure the query layer did not mutate or reconstruct
    # the service-layer update payload.
    assert query.update.call_args.args[0] is updates


def test_update_branding_returns_none_when_update_matches_no_record(mocker):
    updates = {
        "primary_color": "#FFFFFF",
    }

    execute = mocker.Mock(
        return_value=mocker.Mock(
            data=None,
        )
    )

    query = mocker.Mock()
    query.update.return_value = query
    query.eq.return_value = query
    query.select.return_value = query
    query.maybe_single.return_value = query
    query.execute = execute

    supabase = mocker.patch.object(
        queries,
        "supabase_admin",
    )

    supabase.table.return_value = query

    result = queries.update_branding(
        organization_id=ORGANIZATION_ID,
        updates=updates,
    )

    assert result is None

    query.update.assert_called_once_with(updates)

    query.eq.assert_called_once_with(
        "id",
        str(ORGANIZATION_ID),
    )

    query.maybe_single.assert_called_once_with()
    execute.assert_called_once_with()