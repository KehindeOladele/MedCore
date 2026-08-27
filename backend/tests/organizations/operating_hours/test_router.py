from uuid import UUID

import pytest

from app.modules.organizations.operating_hours import router

from app.modules.organizations.operating_hours.exceptions import (
    OperatingHoursConflictError,
    OperatingHoursNotFoundError,
)

from tests.factories.constants import ORGANIZATION_ID, USER_ID, OPERATING_HOURS_ID
from tests.factories.operating_hours import response_data


ENTRY_ID = OPERATING_HOURS_ID

BASE_URL = f"/organizations/{ORGANIZATION_ID}/operating-hours"





# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------


def test_create_route_returns_201_and_delegates_to_service(
    authenticated_client,
    mocker,
):
    create = mocker.patch.object(
        router,
        "create_operating_hours",
        return_value=response_data(),
    )

    payload = {
        "day_of_week": 0,
        "slot_index": 0,
        "opens_at": "08:00:00",
        "closes_at": "16:00:00",
        "is_closed": False,
    }

    response = authenticated_client.post(
        BASE_URL,
        json=payload,
    )

    assert response.status_code == 201
    assert response.json()["id"] == str(ENTRY_ID)

    create.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
        payload=mocker.ANY,
        actor_id=USER_ID,
    )


def test_create_route_accepts_closed_day(
    authenticated_client,
    mocker,
):
    create = mocker.patch.object(
        router,
        "create_operating_hours",
        return_value=response_data(
            day_of_week=6,
            slot_index=0,
            opens_at=None,
            closes_at=None,
            is_closed=True,
        ),
    )

    response = authenticated_client.post(
        BASE_URL,
        json={
            "day_of_week": 6,
            "is_closed": True,
        },
    )

    assert response.status_code == 201
    assert response.json()["is_closed"] is True

    create.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
        payload=mocker.ANY,
        actor_id=USER_ID,
    )


def test_create_route_rejects_invalid_open_window(
    authenticated_client,
    mocker,
):
    create = mocker.patch.object(
        router,
        "create_operating_hours",
    )

    response = authenticated_client.post(
        BASE_URL,
        json={
            "day_of_week": 0,
            "opens_at": "17:00:00",
            "closes_at": "08:00:00",
        },
    )

    assert response.status_code == 422
    create.assert_not_called()


def test_create_route_returns_409_on_conflict(
    authenticated_client,
    mocker,
):
    mocker.patch.object(
        router,
        "create_operating_hours",
        side_effect=OperatingHoursConflictError(),
    )

    response = authenticated_client.post(
        BASE_URL,
        json={
            "day_of_week": 0,
            "opens_at": "08:00:00",
            "closes_at": "16:00:00",
        },
    )

    assert response.status_code == 409


# ---------------------------------------------------------------------------
# List
# ---------------------------------------------------------------------------


def test_list_route_returns_200_and_delegates_to_service(
    authenticated_client,
    mocker,
):
    list_service = mocker.patch.object(
        router,
        "list_operating_hours",
        return_value=[
            response_data(),
            response_data(
                id="22222222-2222-2222-2222-222222222222",
                slot_index=1,
                opens_at="17:00:00",
                closes_at="20:00:00",
            ),
        ],
    )

    response = authenticated_client.get(BASE_URL)

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["day_of_week"] == 0

    list_service.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
    )


def test_list_route_returns_empty_list(
    authenticated_client,
    mocker,
):
    list_service = mocker.patch.object(
        router,
        "list_operating_hours",
        return_value=[],
    )

    response = authenticated_client.get(BASE_URL)

    assert response.status_code == 200
    assert response.json() == []

    list_service.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
    )


# ---------------------------------------------------------------------------
# Get
# ---------------------------------------------------------------------------


def test_get_route_returns_200_and_delegates_to_service(
    authenticated_client,
    mocker,
):
    get = mocker.patch.object(
        router,
        "get_operating_hours",
        return_value=response_data(),
    )

    response = authenticated_client.get(
        f"{BASE_URL}/{ENTRY_ID}",
    )

    assert response.status_code == 200
    assert response.json()["id"] == str(ENTRY_ID)

    get.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
        operating_hours_id=OPERATING_HOURS_ID,
    )


def test_get_route_returns_404_when_entry_is_missing(
    authenticated_client,
    mocker,
):
    mocker.patch.object(
        router,
        "get_operating_hours",
        side_effect=OperatingHoursNotFoundError(),
    )

    response = authenticated_client.get(
        f"{BASE_URL}/{ENTRY_ID}",
    )

    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------


def test_update_route_returns_200_and_delegates_to_service(
    authenticated_client,
    mocker,
):
    update = mocker.patch.object(
        router,
        "update_operating_hours",
        return_value=response_data(
            closes_at="18:00:00",
        ),
    )

    response = authenticated_client.patch(
        f"{BASE_URL}/{ENTRY_ID}",
        json={
            "closes_at": "18:00:00",
        },
    )

    assert response.status_code == 200
    assert response.json()["closes_at"] == "18:00:00"

    update.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
        operating_hours_id=OPERATING_HOURS_ID,
        payload=mocker.ANY,
        actor_id=USER_ID,
    )


def test_update_route_returns_404_when_entry_is_missing(
    authenticated_client,
    mocker,
):
    mocker.patch.object(
        router,
        "update_operating_hours",
        side_effect=OperatingHoursNotFoundError(),
    )

    response = authenticated_client.patch(
        f"{BASE_URL}/{ENTRY_ID}",
        json={
            "closes_at": "18:00:00",
        },
    )

    assert response.status_code == 404


def test_update_route_returns_409_on_conflict(
    authenticated_client,
    mocker,
):
    mocker.patch.object(
        router,
        "update_operating_hours",
        side_effect=OperatingHoursConflictError(),
    )

    response = authenticated_client.patch(
        f"{BASE_URL}/{ENTRY_ID}",
        json={
            "closes_at": "18:00:00",
        },
    )

    assert response.status_code == 409


def test_update_route_rejects_invalid_time_format(
    authenticated_client,
    mocker,
):
    update = mocker.patch.object(
        router,
        "update_operating_hours",
    )

    response = authenticated_client.patch(
        f"{BASE_URL}/{ENTRY_ID}",
        json={
            "closes_at": "not-a-time",
        },
    )

    assert response.status_code == 422
    update.assert_not_called()


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------


def test_delete_route_returns_204_and_delegates_to_service(
    authenticated_client,
    mocker,
):
    remove = mocker.patch.object(
        router,
        "delete_operating_hours",
    )

    response = authenticated_client.delete(
        f"{BASE_URL}/{ENTRY_ID}",
    )

    assert response.status_code == 204
    assert response.content == b""

    remove.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
        operating_hours_id=OPERATING_HOURS_ID,
        actor_id=USER_ID,
    )


def test_delete_route_returns_404_when_entry_is_missing(
    authenticated_client,
    mocker,
):
    mocker.patch.object(
        router,
        "delete_operating_hours",
        side_effect=OperatingHoursNotFoundError(),
    )

    response = authenticated_client.delete(
        f"{BASE_URL}/{ENTRY_ID}",
    )

    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "method,path",
    [
        ("GET", BASE_URL),
        ("POST", BASE_URL),
        ("GET", f"{BASE_URL}/{ENTRY_ID}"),
        ("PATCH", f"{BASE_URL}/{ENTRY_ID}"),
        ("DELETE", f"{BASE_URL}/{ENTRY_ID}"),
    ],
)
def test_routes_require_authentication(
    client,
    method,
    path,
):
    response = client.request(
        method,
        path,
        json=(
            {
                "day_of_week": 0,
                "opens_at": "08:00:00",
                "closes_at": "16:00:00",
            }
            if method == "POST"
            else {
                "closes_at": "18:00:00",
            }
            if method == "PATCH"
            else None
        ),
    )

    assert response.status_code == 401