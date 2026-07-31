import pytest

from app.modules.organizations.departments import queries

from tests.helpers.responses import (
    mock_empty,
)
from tests.helpers.supabase import (
    patch_supabase_empty,
    patch_supabase_list,
    patch_supabase_single,
    patch_supabase_table,
)


SUPABASE_TARGET = (
    "app.modules.organizations.departments.queries.supabase"
)


# ---------------------------------------------------------------------
# create_department
# ---------------------------------------------------------------------

def test_create_department(
    mocker,
    department_data,
):
    _, chain = patch_supabase_single(
        mocker,
        SUPABASE_TARGET,
        department_data,
    )

    result = queries.create_department(department_data)

    chain.insert.assert_called_once_with(department_data)
    chain.execute.assert_called_once()

    assert result == department_data


# ---------------------------------------------------------------------
# get_department
# ---------------------------------------------------------------------

def test_get_department(
    mocker,
    department_data,
):
    _, chain = patch_supabase_single(
        mocker,
        SUPABASE_TARGET,
        department_data,
    )

    result = queries.get_department(
        organization_id=department_data["organization_id"],
        department_id=department_data["id"],
    )

    chain.select.assert_called_once()
    chain.execute.assert_called_once()

    assert result == department_data


def test_get_department_not_found(
    mocker,
):
    _, chain = patch_supabase_empty(
        mocker,
        SUPABASE_TARGET,
    )

    result = queries.get_department(
        organization_id="org-1",
        department_id="dept-1",
    )

    chain.execute.assert_called_once()

    assert result is None


# ---------------------------------------------------------------------
# list_departments
# ---------------------------------------------------------------------

def test_list_departments(
    mocker,
    department_data,
):
    _, chain = patch_supabase_list(
        mocker,
        SUPABASE_TARGET,
        [department_data],
    )

    result = queries.list_departments(
        department_data["organization_id"]
    )

    chain.select.assert_called_once()
    chain.order.assert_called_once()

    assert result == [department_data]


def test_list_departments_empty(
    mocker,
):
    _, chain = patch_supabase_empty(
        mocker,
        SUPABASE_TARGET,
    )

    result = queries.list_departments("org-1")

    chain.execute.assert_called_once()

    assert result == []


# ---------------------------------------------------------------------
# department_exists
# ---------------------------------------------------------------------

def test_department_exists_true(
    mocker,
    department_data,
):
    patch_supabase_single(
        mocker,
        SUPABASE_TARGET,
        department_data,
    )

    assert queries.department_exists(
        department_data["organization_id"],
        department_data["name"],
    ) is True


def test_department_exists_false(
    mocker,
):
    patch_supabase_empty(
        mocker,
        SUPABASE_TARGET,
    )

    assert queries.department_exists(
        "org-1",
        "Radiology",
    ) is False


# ---------------------------------------------------------------------
# update_department
# ---------------------------------------------------------------------

def test_update_department(
    mocker,
    department_data,
    updated_department_data,
):
    _, chain = patch_supabase_single(
        mocker,
        SUPABASE_TARGET,
        updated_department_data,
    )

    result = queries.update_department(
        department_id=department_data["id"],
        payload=updated_department_data,
    )

    chain.update.assert_called_once_with(updated_department_data)
    chain.execute.assert_called_once()

    assert result == updated_department_data


# ---------------------------------------------------------------------
# soft_delete_department
# ---------------------------------------------------------------------

def test_soft_delete_department(
    mocker,
):
    _, chain = patch_supabase_empty(
        mocker,
        SUPABASE_TARGET,
    )

    queries.soft_delete_department("dept-1")

    chain.update.assert_called_once()
    chain.execute.assert_called_once()


# ---------------------------------------------------------------------
# list_department_children
# ---------------------------------------------------------------------

def test_list_department_children(
    mocker,
    department_data,
):
    _, chain = patch_supabase_list(
        mocker,
        SUPABASE_TARGET,
        [department_data],
    )

    result = queries.list_department_children(
        organization_id=department_data["organization_id"],
        parent_department_id=department_data["parent_department_id"],
    )

    chain.select.assert_called_once()
    chain.execute.assert_called_once()

    assert result == [department_data]


# ---------------------------------------------------------------------
# has_child_departments
# ---------------------------------------------------------------------

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


def test_has_child_departments_false(
    mocker,
):
    mocker.patch.object(
        queries,
        "list_department_children",
        return_value=[],
    )

    assert (
        queries.has_child_departments(
            "org-1",
            "dept-1",
        )
        is False
    )