import pytest

from app.modules.organizations.departments import queries
from tests.helpers.responses import make_supabase_response



# ---------------------------
# CREATE TABLE QUERY TEST
# ---------------------------
def test_create_department(mocker, department_data):
    """Should insert a department and return the created record."""

    execute = mocker.Mock(
        return_value=make_supabase_response([department_data])
    )

    insert = mocker.Mock(return_value=mocker.Mock(execute=execute))

    table = mocker.Mock(return_value=mocker.Mock(insert=insert))

    mocker.patch.object(
        queries,
        "supabase",
        mocker.Mock(table=table),
    )

    result = queries.create_department(department_data)

    table.assert_called_once_with("departments")
    insert.assert_called_once_with(department_data)
    execute.assert_called_once()

    assert result == department_data


# ---------------------------
# GET TABLE QUERY TEST
# ---------------------------
def test_get_department(mocker, department_data):

    execute = mocker.Mock(
        return_value=make_supabase_response([department_data])
    )

    single = mocker.Mock(return_value=mocker.Mock(execute=execute))
    eq = mocker.Mock(return_value=mocker.Mock(single=single))

    select = mocker.Mock(return_value=mocker.Mock(eq=eq))

    table = mocker.Mock(return_value=mocker.Mock(select=select))

    mocker.patch.object(
        queries,
        "supabase",
        mocker.Mock(table=table),
    )

    result = queries.get_department(
        organization_id=department_data["organization_id"],
        department_id=department_data["id"],
    )

    assert result == department_data
    

# ---------------------------
# LIST TABLE QUERY TEST
# ---------------------------
def test_list_departments(mocker, department_data):

    execute = mocker.Mock(
        return_value=make_supabase_response([department_data])
    )

    order = mocker.Mock(return_value=mocker.Mock(execute=execute))
    eq = mocker.Mock(return_value=mocker.Mock(order=order))
    select = mocker.Mock(return_value=mocker.Mock(eq=eq))

    table = mocker.Mock(return_value=mocker.Mock(select=select))

    mocker.patch.object(
        queries,
        "supabase",
        mocker.Mock(table=table),
    )

    result = queries.list_departments(
        department_data["organization_id"]
    )

    assert len(result) == 1
    assert result[0]["name"] == department_data["name"]
        

# --------------------------------
# DEPARTMENT EXIST TRUE QUERY TEST
# --------------------------------
def test_department_exists_true(mocker, department_data):

    execute = mocker.Mock(
        return_value=make_supabase_response([department_data])
    )

    limit = mocker.Mock(return_value=mocker.Mock(execute=execute))
    eq = mocker.Mock(return_value=mocker.Mock(limit=limit))
    select = mocker.Mock(return_value=mocker.Mock(eq=eq))

    table = mocker.Mock(return_value=mocker.Mock(select=select))

    mocker.patch.object(
        queries,
        "supabase",
        mocker.Mock(table=table),
    )

    assert (
        queries.department_exists(
            department_data["organization_id"],
            department_data["name"],
        )
        is True
    )
        

# ---------------------------------
# DEPARTMENT EXIST FALSE QUERY TEST
# ---------------------------------
def test_department_exists_false(mocker):

    execute = mocker.Mock(
        return_value=make_supabase_response([])
    )

    limit = mocker.Mock(return_value=mocker.Mock(execute=execute))
    eq = mocker.Mock(return_value=mocker.Mock(limit=limit))
    select = mocker.Mock(return_value=mocker.Mock(eq=eq))

    table = mocker.Mock(return_value=mocker.Mock(select=select))

    mocker.patch.object(
        queries,
        "supabase",
        mocker.Mock(table=table),
    )

    assert (
        queries.department_exists(
            "org1",
            "Radiology",
        )
        is False
    )
        

# --------------------------------
# UPDATE DEPARTMENT QUERY TEST
# --------------------------------
def test_update_department(
    mocker,
    department_data,
    updated_department_data,
):

    execute = mocker.Mock(
        return_value=make_supabase_response([updated_department_data])
    )

    single = mocker.Mock(return_value=mocker.Mock(execute=execute))
    eq = mocker.Mock(return_value=mocker.Mock(single=single))
    update = mocker.Mock(return_value=mocker.Mock(eq=eq))

    table = mocker.Mock(return_value=mocker.Mock(update=update))

    mocker.patch.object(
        queries,
        "supabase",
        mocker.Mock(table=table),
    )

    result = queries.update_department(
        department_data["id"],
        updated_department_data,
    )

    assert result["name"] == updated_department_data["name"]
            

# --------------------------------
# DELETE DEPARTMENT QUERY TEST
# --------------------------------
def test_soft_delete_department(mocker):

    execute = mocker.Mock(
        return_value=make_supabase_response([])
    )

    eq = mocker.Mock(return_value=mocker.Mock(execute=execute))
    update = mocker.Mock(return_value=mocker.Mock(eq=eq))

    table = mocker.Mock(return_value=mocker.Mock(update=update))

    mocker.patch.object(
        queries,
        "supabase",
        mocker.Mock(table=table),
    )

    queries.soft_delete_department("dept1")

    execute.assert_called_once()
                

# -----------------------------------
# LIST DEPARTMENT CHILDREN QUERY TEST
# -----------------------------------
def test_list_department_children(
    mocker,
    department_data,
):

    execute = mocker.Mock(
        return_value=make_supabase_response([department_data])
    )

    eq = mocker.Mock(return_value=mocker.Mock(execute=execute))
    select = mocker.Mock(return_value=mocker.Mock(eq=eq))

    table = mocker.Mock(return_value=mocker.Mock(select=select))

    mocker.patch.object(
        queries,
        "supabase",
        mocker.Mock(table=table),
    )

    result = queries.list_department_children(
        department_data["organization_id"],
        department_data["parent_department_id"],
    )

    assert isinstance(result, list)
                

# ---------------------------------------
# DEPARTMENT HAS CHILDREN TRUE QUERY TEST
# ---------------------------------------
def test_has_child_departments_true(
    mocker,
    department_data,
):

    mocker.patch.object(
        queries,
        "list_department_children",
        return_value=[department_data],
    )

    assert (
        queries.has_child_departments(
            department_data["organization_id"],
            department_data["parent_department_id"],
        )
        is True
    )
                

# ----------------------------------------
# DEPARTMENT HAS CHILDREN FALSE QUERY TEST
# ----------------------------------------
def test_has_child_departments_false(mocker):

    mocker.patch.object(
        queries,
        "list_department_children",
        return_value=[],
    )

    assert (
        queries.has_child_departments(
            "org1",
            "dept1",
        )
        is False
    )