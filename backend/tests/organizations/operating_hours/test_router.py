import pytest
from uuid import UUID

from app.modules.organizations.operating_hours import router
from app.modules.organizations.operating_hours.exceptions import OperatingHoursConflictError, OperatingHoursNotFoundError
from tests.factories.constants import ORGANIZATION_ID, USER_ID


ENTRY_ID = "11111111-1111-1111-1111-111111111111"
BASE_URL = f"/organizations/{ORGANIZATION_ID}/operating-hours"


def response_data():
    return {"id": ENTRY_ID, "organization_id": str(ORGANIZATION_ID), "day_of_week": 0, "slot_index": 0, "opens_at": "08:00:00", "closes_at": "16:00:00", "is_closed": False, "created_by": str(USER_ID), "updated_by": str(USER_ID), "deleted_at": None, "created_at": "2026-01-01T00:00:00Z", "updated_at": "2026-01-01T00:00:00Z"}


def test_create_route_delegates_to_service(authenticated_client, mocker):
    create = mocker.patch.object(router, "create_operating_hours", return_value=response_data())
    response = authenticated_client.post(BASE_URL, json={"day_of_week": 0, "opens_at": "08:00:00", "closes_at": "16:00:00"})
    assert response.status_code == 201
    create.assert_called_once_with(organization_id=ORGANIZATION_ID, payload=mocker.ANY, actor_id=USER_ID)


def test_list_route_delegates_to_service(authenticated_client, mocker):
    list_service = mocker.patch.object(router, "list_operating_hours", return_value=[response_data()])
    response = authenticated_client.get(BASE_URL)
    assert response.status_code == 200
    assert response.json()[0]["day_of_week"] == 0
    list_service.assert_called_once_with(organization_id=ORGANIZATION_ID)


def test_get_not_found_is_404(authenticated_client, mocker):
    mocker.patch.object(router, "get_operating_hours", side_effect=OperatingHoursNotFoundError())
    assert authenticated_client.get(f"{BASE_URL}/{ENTRY_ID}").status_code == 404


def test_create_conflict_is_409(authenticated_client, mocker):
    mocker.patch.object(router, "create_operating_hours", side_effect=OperatingHoursConflictError())
    response = authenticated_client.post(BASE_URL, json={"day_of_week": 0, "opens_at": "08:00:00", "closes_at": "16:00:00"})
    assert response.status_code == 409


def test_update_route_delegates_to_service(authenticated_client, mocker):
    update = mocker.patch.object(router, "update_operating_hours", return_value=response_data())
    response = authenticated_client.patch(f"{BASE_URL}/{ENTRY_ID}", json={"closes_at": "18:00:00"})
    assert response.status_code == 200
    update.assert_called_once_with(organization_id=ORGANIZATION_ID, operating_hours_id=UUID(ENTRY_ID), payload=mocker.ANY, actor_id=USER_ID)


def test_delete_route_returns_no_content(authenticated_client, mocker):
    remove = mocker.patch.object(router, "delete_operating_hours")
    response = authenticated_client.delete(f"{BASE_URL}/{ENTRY_ID}")
    assert response.status_code == 204
    remove.assert_called_once_with(organization_id=ORGANIZATION_ID, operating_hours_id=UUID(ENTRY_ID), actor_id=USER_ID)


@pytest.mark.parametrize("method,path", [("GET", BASE_URL), ("POST", BASE_URL), ("PATCH", f"{BASE_URL}/{ENTRY_ID}"), ("DELETE", f"{BASE_URL}/{ENTRY_ID}")])
def test_routes_require_authentication(client, method, path):
    assert client.request(method, path).status_code == 401
