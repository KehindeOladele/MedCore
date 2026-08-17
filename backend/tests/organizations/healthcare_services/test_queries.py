from uuid import UUID

from app.modules.organizations.healthcare_services import queries


ORGANIZATION_ID = UUID(
    "0b7d7b1b-208f-4618-9972-c652672a6fb9"
)

HEALTHCARE_SERVICE_ID = UUID(
    "07e46ce0-1701-4479-be7c-3841e7661ffe"
)

DEPARTMENT_ID = UUID(
    "11111111-1111-1111-1111-111111111111"
)

USER_ID = UUID(
    "22222222-2222-2222-2222-222222222222"
)


# =========================================================
# CREATE
# =========================================================

def test_create_healthcare_service(
    mocker,
    healthcare_service_create,
):
    response_data = {
        "id": str(HEALTHCARE_SERVICE_ID),
        "organization_id": str(ORGANIZATION_ID),
        "name": "Cardiology",
    }

    execute = mocker.Mock(
        return_value=mocker.Mock(
            data=[response_data]
        )
    )

    query = mocker.Mock()
    query.insert.return_value = query
    query.execute = execute

    supabase = mocker.patch.object(
        queries,
        "supabase",
    )

    supabase.table.return_value = query

    result = queries.create_healthcare_service(
        organization_id=ORGANIZATION_ID,
        payload=healthcare_service_create,
        created_by=USER_ID,
    )

    assert result == response_data

    supabase.table.assert_called_once_with(
        queries.TABLE
    )

    query.insert.assert_called_once()

    inserted_data = query.insert.call_args.args[0]

    assert inserted_data["organization_id"] == str(
        ORGANIZATION_ID
    )

    assert inserted_data["created_by"] == str(USER_ID)
    assert inserted_data["updated_by"] == str(USER_ID)

    execute.assert_called_once()


# =========================================================
# GET
# =========================================================

def test_get_healthcare_service_found(
    mocker,
):
    response_data = {
        "id": str(HEALTHCARE_SERVICE_ID),
        "organization_id": str(ORGANIZATION_ID),
        "name": "Cardiology",
    }

    execute = mocker.Mock(
        return_value=mocker.Mock(
            data=[response_data]
        )
    )

    query = mocker.Mock()
    query.select.return_value = query
    query.eq.return_value = query
    query.is_.return_value = query
    query.limit.return_value = query
    query.execute = execute

    supabase = mocker.patch.object(
        queries,
        "supabase",
    )

    supabase.table.return_value = query

    result = queries.get_healthcare_service(
        organization_id=ORGANIZATION_ID,
        healthcare_service_id=HEALTHCARE_SERVICE_ID,
    )

    assert result == response_data

    query.select.assert_called_once_with("*")

    query.eq.assert_any_call(
        "organization_id",
        str(ORGANIZATION_ID),
    )

    query.eq.assert_any_call(
        "id",
        str(HEALTHCARE_SERVICE_ID),
    )

    query.is_.assert_called_once_with(
        "deleted_at",
        "null",
    )

    query.limit.assert_called_once_with(1)

    execute.assert_called_once()


def test_get_healthcare_service_not_found(
    mocker,
):
    execute = mocker.Mock(
        return_value=mocker.Mock(
            data=[]
        )
    )

    query = mocker.Mock()
    query.select.return_value = query
    query.eq.return_value = query
    query.is_.return_value = query
    query.limit.return_value = query
    query.execute = execute

    supabase = mocker.patch.object(
        queries,
        "supabase",
    )

    supabase.table.return_value = query

    result = queries.get_healthcare_service(
        organization_id=ORGANIZATION_ID,
        healthcare_service_id=HEALTHCARE_SERVICE_ID,
    )

    assert result is None


# =========================================================
# LIST
# =========================================================

def test_list_healthcare_services(
    mocker,
):
    response_data = [
        {
            "id": str(HEALTHCARE_SERVICE_ID),
            "organization_id": str(ORGANIZATION_ID),
            "name": "Cardiology",
        },
        {
            "id": "33333333-3333-3333-3333-333333333333",
            "organization_id": str(ORGANIZATION_ID),
            "name": "Radiology",
        },
    ]

    execute = mocker.Mock(
        return_value=mocker.Mock(
            data=response_data
        )
    )

    query = mocker.Mock()
    query.select.return_value = query
    query.eq.return_value = query
    query.is_.return_value = query
    query.order.return_value = query
    query.execute = execute

    supabase = mocker.patch.object(
        queries,
        "supabase",
    )

    supabase.table.return_value = query

    result = queries.list_healthcare_services(
        organization_id=ORGANIZATION_ID,
    )

    assert result == response_data

    query.eq.assert_called_once_with(
        "organization_id",
        str(ORGANIZATION_ID),
    )

    query.is_.assert_called_once_with(
        "deleted_at",
        "null",
    )

    assert query.order.call_count == 2

    query.order.assert_any_call(
        "display_order"
    )

    query.order.assert_any_call(
        "name"
    )

    execute.assert_called_once()


def test_list_healthcare_services_active_only(
    mocker,
):
    response_data = [
        {
            "id": str(HEALTHCARE_SERVICE_ID),
            "organization_id": str(ORGANIZATION_ID),
            "name": "Cardiology",
            "active": True,
        }
    ]

    execute = mocker.Mock(
        return_value=mocker.Mock(
            data=response_data
        )
    )

    query = mocker.Mock()
    query.select.return_value = query
    query.eq.return_value = query
    query.is_.return_value = query
    query.order.return_value = query
    query.execute = execute

    supabase = mocker.patch.object(
        queries,
        "supabase",
    )

    supabase.table.return_value = query

    result = queries.list_healthcare_services(
        organization_id=ORGANIZATION_ID,
        active_only=True,
    )

    assert result == response_data

    query.eq.assert_any_call(
        "active",
        True,
    )

    execute.assert_called_once()


# =========================================================
# UPDATE
# =========================================================

def test_update_healthcare_service(
    mocker,
    healthcare_service_update,
):
    response_data = {
        "id": str(HEALTHCARE_SERVICE_ID),
        "organization_id": str(ORGANIZATION_ID),
        "name": "Updated Cardiology",
        "updated_by": str(USER_ID),
    }

    execute = mocker.Mock(
        return_value=mocker.Mock(
            data=[response_data]
        )
    )

    query = mocker.Mock()
    query.update.return_value = query
    query.eq.return_value = query
    query.execute = execute

    supabase = mocker.patch.object(
        queries,
        "supabase",
    )

    supabase.table.return_value = query

    result = queries.update_healthcare_service(
        organization_id=ORGANIZATION_ID,
        healthcare_service_id=HEALTHCARE_SERVICE_ID,
        payload=healthcare_service_update,
        updated_by=USER_ID,
    )

    assert result == response_data

    query.eq.assert_any_call(
        "organization_id",
        str(ORGANIZATION_ID),
    )

    query.eq.assert_any_call(
        "id",
        str(HEALTHCARE_SERVICE_ID),
    )

    updated_data = query.update.call_args.args[0]

    assert updated_data["updated_by"] == str(USER_ID)

    execute.assert_called_once()


# =========================================================
# DELETE
# =========================================================

def test_delete_healthcare_service(
    mocker,
):
    response_data = {
        "id": str(HEALTHCARE_SERVICE_ID),
        "organization_id": str(ORGANIZATION_ID),
        "active": False,
    }

    execute = mocker.Mock(
        return_value=mocker.Mock(
            data=[response_data]
        )
    )

    query = mocker.Mock()
    query.update.return_value = query
    query.eq.return_value = query
    query.execute = execute

    supabase = mocker.patch.object(
        queries,
        "supabase",
    )

    supabase.table.return_value = query

    result = queries.delete_healthcare_service(
        organization_id=ORGANIZATION_ID,
        healthcare_service_id=HEALTHCARE_SERVICE_ID,
        deleted_by=USER_ID,
    )

    assert result == response_data

    updated_data = query.update.call_args.args[0]

    assert updated_data["active"] is False
    assert "deleted_at" in updated_data
    assert updated_data["updated_by"] == str(USER_ID)

    query.eq.assert_any_call(
        "organization_id",
        str(ORGANIZATION_ID),
    )

    query.eq.assert_any_call(
        "id",
        str(HEALTHCARE_SERVICE_ID),
    )

    execute.assert_called_once()


# =========================================================
# GET BY NAME
# =========================================================

def test_get_healthcare_service_by_name_found(
    mocker,
):
    response_data = {
        "id": str(HEALTHCARE_SERVICE_ID),
        "organization_id": str(ORGANIZATION_ID),
        "name": "Cardiology",
    }

    execute = mocker.Mock(
        return_value=mocker.Mock(
            data=[response_data]
        )
    )

    query = mocker.Mock()
    query.select.return_value = query
    query.eq.return_value = query
    query.is_.return_value = query
    query.limit.return_value = query
    query.execute = execute

    supabase = mocker.patch.object(
        queries,
        "supabase",
    )

    supabase.table.return_value = query

    result = queries.get_healthcare_service_by_name(
        organization_id=ORGANIZATION_ID,
        name="Cardiology",
    )

    assert result == response_data

    query.eq.assert_any_call(
        "organization_id",
        str(ORGANIZATION_ID),
    )

    query.eq.assert_any_call(
        "name",
        "Cardiology",
    )

    query.is_.assert_called_once_with(
        "deleted_at",
        "null",
    )

    query.limit.assert_called_once_with(1)


def test_get_healthcare_service_by_name_not_found(
    mocker,
):
    execute = mocker.Mock(
        return_value=mocker.Mock(
            data=[]
        )
    )

    query = mocker.Mock()
    query.select.return_value = query
    query.eq.return_value = query
    query.is_.return_value = query
    query.limit.return_value = query
    query.execute = execute

    supabase = mocker.patch.object(
        queries,
        "supabase",
    )

    supabase.table.return_value = query

    result = queries.get_healthcare_service_by_name(
        organization_id=ORGANIZATION_ID,
        name="Cardiology",
    )

    assert result is None


# =========================================================
# DEPARTMENT FILTER
# =========================================================

def test_list_department_healthcare_services(
    mocker,
):
    response_data = [
        {
            "id": str(HEALTHCARE_SERVICE_ID),
            "organization_id": str(ORGANIZATION_ID),
            "department_id": str(DEPARTMENT_ID),
            "name": "Cardiology",
        }
    ]

    execute = mocker.Mock(
        return_value=mocker.Mock(
            data=response_data
        )
    )

    query = mocker.Mock()
    query.select.return_value = query
    query.eq.return_value = query
    query.is_.return_value = query
    query.order.return_value = query
    query.execute = execute

    supabase = mocker.patch.object(
        queries,
        "supabase",
    )

    supabase.table.return_value = query

    result = queries.list_department_healthcare_services(
        organization_id=ORGANIZATION_ID,
        department_id=DEPARTMENT_ID,
    )

    assert result == response_data

    query.eq.assert_any_call(
        "organization_id",
        str(ORGANIZATION_ID),
    )

    query.eq.assert_any_call(
        "department_id",
        str(DEPARTMENT_ID),
    )

    query.is_.assert_called_once_with(
        "deleted_at",
        "null",
    )

    query.order.assert_any_call(
        "display_order"
    )

    query.order.assert_any_call(
        "name"
    )

    execute.assert_called_once()