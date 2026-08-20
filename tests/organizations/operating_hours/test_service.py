from datetime import datetime, time, timezone

import pytest

from app.modules.organizations.operating_hours import service
from app.modules.organizations.operating_hours.exceptions import OperatingHoursConflictError, OperatingHoursNotFoundError
from app.modules.organizations.operating_hours.schemas import OperatingHoursCreate, OperatingHoursUpdate
from tests.factories.constants import ORGANIZATION_ID, USER_ID


ENTRY_ID = "11111111-1111-1111-1111-111111111111"


def entry(**overrides):
    value = {
        "id": ENTRY_ID, "organization_id": str(ORGANIZATION_ID), "day_of_week": 0,
        "slot_index": 0, "opens_at": "08:00:00", "closes_at": "16:00:00",
        "is_closed": False, "created_by": str(USER_ID), "updated_by": str(USER_ID),
        "deleted_at": None, "created_at": datetime.now(timezone.utc).isoformat(), "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    value.update(overrides)
    return value


def active_organization(mocker):
    mocker.patch.object(service.organization_queries, "get_organization", return_value={"active": True})


def test_create_persists_a_valid_window_and_records_activity(mocker):
    active_organization(mocker)
    mocker.patch.object(service.queries, "list_operating_hours", return_value=[])
    create = mocker.patch.object(service.queries, "create_operating_hours", return_value=entry())
    activity = mocker.patch.object(service, "_record_activity")
    result = service.create_operating_hours(organization_id=ORGANIZATION_ID, payload=OperatingHoursCreate(day_of_week=0, opens_at=time(8), closes_at=time(16)), actor_id=USER_ID)
    assert str(result.id) == ENTRY_ID
    assert create.call_args.args[0]["organization_id"] == str(ORGANIZATION_ID)
    activity.assert_called_once()


def test_create_rejects_an_overlapping_window(mocker):
    active_organization(mocker)
    mocker.patch.object(service.queries, "list_operating_hours", return_value=[entry(opens_at="09:00:00", closes_at="17:00:00")])
    with pytest.raises(OperatingHoursConflictError):
        service.create_operating_hours(organization_id=ORGANIZATION_ID, payload=OperatingHoursCreate(day_of_week=0, opens_at=time(8), closes_at=time(10)), actor_id=USER_ID)


def test_create_rejects_a_duplicate_slot_index(mocker):
    active_organization(mocker)
    mocker.patch.object(service.queries, "list_operating_hours", return_value=[entry(opens_at="08:00:00", closes_at="10:00:00")])
    with pytest.raises(OperatingHoursConflictError):
        service.create_operating_hours(organization_id=ORGANIZATION_ID, payload=OperatingHoursCreate(day_of_week=0, opens_at=time(11), closes_at=time(12)), actor_id=USER_ID)


def test_create_rejects_a_closed_marker_when_windows_exist(mocker):
    active_organization(mocker)
    mocker.patch.object(service.queries, "list_operating_hours", return_value=[entry()])
    with pytest.raises(OperatingHoursConflictError):
        service.create_operating_hours(organization_id=ORGANIZATION_ID, payload=OperatingHoursCreate(day_of_week=0, is_closed=True), actor_id=USER_ID)


def test_get_raises_when_entry_is_not_in_organization(mocker):
    mocker.patch.object(service.queries, "get_operating_hours", return_value=None)
    with pytest.raises(OperatingHoursNotFoundError):
        service.get_operating_hours(organization_id=ORGANIZATION_ID, operating_hours_id=ENTRY_ID)


def test_update_validates_the_complete_merged_window(mocker):
    active_organization(mocker)
    mocker.patch.object(service.queries, "get_operating_hours", return_value=entry())
    mocker.patch.object(service.queries, "list_operating_hours", return_value=[])
    update = mocker.patch.object(service.queries, "update_operating_hours", return_value=entry(closes_at="18:00:00"))
    mocker.patch.object(service, "_record_activity")
    result = service.update_operating_hours(organization_id=ORGANIZATION_ID, operating_hours_id=ENTRY_ID, payload=OperatingHoursUpdate(closes_at=time(18)), actor_id=USER_ID)
    assert result.closes_at == time(18)
    assert update.call_args.args[2]["closes_at"] == "18:00:00"


def test_delete_soft_deletes_and_audits(mocker):
    active_organization(mocker)
    mocker.patch.object(service.queries, "get_operating_hours", return_value=entry())
    remove = mocker.patch.object(service.queries, "soft_delete_operating_hours", return_value=entry(deleted_at=datetime.now(timezone.utc).isoformat()))
    activity = mocker.patch.object(service, "_record_activity")
    service.delete_operating_hours(organization_id=ORGANIZATION_ID, operating_hours_id=ENTRY_ID, actor_id=USER_ID)
    assert "deleted_at" in remove.call_args.args[2]
    activity.assert_called_once()
