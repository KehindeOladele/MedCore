import pytest

from uuid import uuid4

from fastapi import status

from app.modules.organizations.departments import router
from app.modules.organizations.departments.schemas import (
    DepartmentResponse,
)
from app.modules.organizations.departments.exceptions import (
    DepartmentAlreadyExistsError,
)



ORGANIZATION_ID = uuid4()

BASE_URL = (
    f"/organizations/{ORGANIZATION_ID}/departments"
)


# ----------------------------
# CREATE DEOARTMENT ROUTE TEST
# ----------------------------
def test_create_department_success(
    authenticated_client,
    authenticated_user,
    mocker,
    create_payload,
    department_data,
):
    create = mocker.patch.object(
        router,
        "create_department_service",
        return_value=DepartmentResponse.model_validate(
            department_data
        ),
    )

    response = authenticated_client.post(
        BASE_URL,
        json=create_payload.model_dump(
            mode="json",
            exclude_none=True,
        ),
    )

    assert response.status_code == status.HTTP_201_CREATED

    body = response.json()

    assert body["id"] == str(
        department_data["id"]
    )

    assert body["name"] == department_data["name"]

    create.assert_called_once()

    _, kwargs = create.call_args

    assert kwargs["organization_id"] == ORGANIZATION_ID

    assert kwargs["actor_id"] == authenticated_user["id"]

    assert kwargs["payload"].name == create_payload.name


# ----------------------------------------
# CREATE DEOARTMENT REQUIREMENT ROUTE TEST
# ----------------------------------------
def test_create_department_requires_authentication(
    client,
    create_payload,
):
    response = client.post(
        BASE_URL,
        json=create_payload.model_dump(
            mode="json",
            exclude_none=True,
        ),
    )

    assert (
        response.status_code
        == status.HTTP_401_UNAUTHORIZED
    )


# --------------------------------------------
# CREATE DEOARTMENT INVALID PAYLOAD ROUTE TEST
# --------------------------------------------
def test_create_department_invalid_payload(
    authenticated_client,
):
    response = authenticated_client.post(
        BASE_URL,
        json={},
    )

    assert (
        response.status_code
        == status.HTTP_422_UNPROCESSABLE_ENTITY
    )


# --------------------------------------------
# CREATE DUPLICATE DEOARTMENT NAME ROUTER TEST
# --------------------------------------------
def test_create_department_duplicate_name(
    authenticated_client,
    mocker,
    create_payload,
):
    mocker.patch.object(
        router,
        "create_department_service",
        side_effect=DepartmentAlreadyExistsError(),
    )

    response = authenticated_client.post(
        BASE_URL,
        json=create_payload.model_dump(
            mode="json",
            exclude_none=True,
        ),
    )

    assert (
        response.status_code
        == status.HTTP_409_CONFLICT
    )


# --------------------------------------------
# VERIFY JSON CONTRACT / SHAPE
# --------------------------------------------
def test_create_department_response_contract(
    authenticated_client,
    mocker,
    create_payload,
    department_data,
):
    mocker.patch.object(
        router,
        "create_department_service",
        return_value=DepartmentResponse.model_validate(
            department_data
        ),
    )

    response = authenticated_client.post(
        BASE_URL,
        json=create_payload.model_dump(
            mode="json",
            exclude_none=True,
        ),
    )

    body = response.json()

    expected = {
        "id",
        "organization_id",
        "parent_department_id",
        "name",
        "code",
        "description",
        "active",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    }

    assert expected.issubset(body.keys())