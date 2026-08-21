from datetime import datetime, time, timezone

import pytest

from app.modules.organizations.operating_hours import service
from app.modules.organizations.exceptions import (
    OrganizationInactiveError,
    OrganizationNotFoundError,
)
from app.modules.organizations.operating_hours.exceptions import (
    OperatingHoursConflictError,
    OperatingHoursNotFoundError,
)
from app.modules.organizations.operating_hours.schemas import (
    OperatingHoursCreate,
    OperatingHoursUpdate,
)
from tests.factories.constants import ORGANIZATION_ID, USER_ID


ENTRY_ID = "11111111-1111-1111-1111-111111111111"
SECOND_ENTRY_ID = "22222222-2222-2222-2222-222222222222"


def entry(**overrides):
    value = {
        "id": ENTRY_ID,
        "organization_id": str(ORGANIZATION_ID),
        "day_of_week": 0,
        "slot_index": 0,
        "opens_at": "08:00:00",
        "closes_at": "16:00:00",
        "is_closed": False,
        "created_by": str(USER_ID),
        "updated_by": str(USER_ID),
        "deleted_at": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    value.update(overrides)
    return value


def active_organization(mocker):
    mocker.patch.object(
        service.organization_queries,
        "get_organization",
        return_value={
            "id": str(ORGANIZATION_ID),
            "active": True,
        },
    )


def inactive_organization(mocker):
    mocker.patch.object(
        service.organization_queries,
        "get_organization",
        return_value={
            "id": str(ORGANIZATION_ID),
            "active": False,
        },
    )


# ============================================================
# Organization validation
# ============================================================


def test_validate_organization_active_success(mocker):
    active_organization(mocker)

    service._validate_organization_active(ORGANIZATION_ID)


def test_validate_organization_active_not_found(mocker):
    mocker.patch.object(
        service.organization_queries,
        "get_organization",
        return_value=None,
    )

    with pytest.raises(OrganizationNotFoundError):
        service._validate_organization_active(ORGANIZATION_ID)


def test_validate_organization_active_rejects_inactive(mocker):
    inactive_organization(mocker)

    with pytest.raises(OrganizationInactiveError):
        service._validate_organization_active(ORGANIZATION_ID)


# ============================================================
# Retrieval helper
# ============================================================


def test_get_or_raise_returns_entry(mocker):
    expected = entry()

    mocker.patch.object(
        service.queries,
        "get_operating_hours",
        return_value=expected,
    )

    result = service._get_or_raise(
        ORGANIZATION_ID,
        ENTRY_ID,
    )

    assert result == expected


def test_get_or_raise_raises_when_missing(mocker):
    mocker.patch.object(
        service.queries,
        "get_operating_hours",
        return_value=None,
    )

    with pytest.raises(OperatingHoursNotFoundError):
        service._get_or_raise(
            ORGANIZATION_ID,
            ENTRY_ID,
        )


# ============================================================
# Conflict validation
# ============================================================

def test_validate_day_conflicts_allows_first_window(mocker):
    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=[],
    )

    candidate = OperatingHoursCreate(
        day_of_week=0,
        slot_index=0,
        opens_at=time(8),
        closes_at=time(12),
    )

    service._validate_day_conflicts(
        organization_id=ORGANIZATION_ID,
        candidate=candidate,
    )


def test_validate_day_conflicts_rejects_duplicate_slot_index(mocker):
    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=[
            entry(
                slot_index=0,
                opens_at="08:00:00",
                closes_at="12:00:00",
            )
        ],
    )

    candidate = OperatingHoursCreate(
        day_of_week=0,
        slot_index=0,
        opens_at=time(13),
        closes_at=time(17),
    )

    with pytest.raises(OperatingHoursConflictError):
        service._validate_day_conflicts(
            organization_id=ORGANIZATION_ID,
            candidate=candidate,
        )


@pytest.mark.parametrize(
    "candidate_open,candidate_close",
    [
        ("08:00", "12:00"),  # exact same window
        ("09:00", "13:00"),  # overlaps at beginning
        ("07:00", "09:00"),  # overlaps at end
        ("10:00", "11:00"),  # contained inside
        ("07:00", "13:00"),  # contains existing window
    ],
)
def test_validate_day_conflicts_rejects_overlapping_windows(
    mocker,
    candidate_open,
    candidate_close,
):
    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=[
            entry(
                slot_index=0,
                opens_at="08:00:00",
                closes_at="12:00:00",
            )
        ],
    )

    candidate = OperatingHoursCreate(
        day_of_week=0,
        slot_index=1,
        opens_at=time.fromisoformat(candidate_open),
        closes_at=time.fromisoformat(candidate_close),
    )

    with pytest.raises(OperatingHoursConflictError):
        service._validate_day_conflicts(
            organization_id=ORGANIZATION_ID,
            candidate=candidate,
        )


@pytest.mark.parametrize(
    "candidate_open,candidate_close",
    [
        ("06:00", "08:00"),
        ("12:00", "16:00"),
        ("13:00", "17:00"),
    ],
)
def test_validate_day_conflicts_allows_adjacent_windows(
    mocker,
    candidate_open,
    candidate_close,
):
    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=[
            entry(
                slot_index=0,
                opens_at="08:00:00",
                closes_at="12:00:00",
            )
        ],
    )

    candidate = OperatingHoursCreate(
        day_of_week=0,
        slot_index=1,
        opens_at=time.fromisoformat(candidate_open),
        closes_at=time.fromisoformat(candidate_close),
    )

    service._validate_day_conflicts(
        organization_id=ORGANIZATION_ID,
        candidate=candidate,
    )


def test_validate_day_conflicts_rejects_closed_marker_when_open_window_exists(
    mocker,
):
    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=[entry()],
    )

    candidate = OperatingHoursCreate(
        day_of_week=0,
        slot_index=1,
        is_closed=True,
    )

    with pytest.raises(OperatingHoursConflictError):
        service._validate_day_conflicts(
            organization_id=ORGANIZATION_ID,
            candidate=candidate,
        )


def test_validate_day_conflicts_rejects_open_window_when_day_has_closed_marker(
    mocker,
):
    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=[
            entry(
                is_closed=True,
                opens_at=None,
                closes_at=None,
            )
        ],
    )

    candidate = OperatingHoursCreate(
        day_of_week=0,
        slot_index=1,
        opens_at=time(8),
        closes_at=time(16),
    )

    with pytest.raises(OperatingHoursConflictError):
        service._validate_day_conflicts(
            organization_id=ORGANIZATION_ID,
            candidate=candidate,
        )


def test_validate_day_conflicts_ignores_excluded_entry(mocker):
    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=[
            entry(
                opens_at="08:00:00",
                closes_at="16:00:00",
            )
        ],
    )

    candidate = OperatingHoursCreate(
        day_of_week=0,
        slot_index=0,
        opens_at=time(8),
        closes_at=time(16),
    )

    service._validate_day_conflicts(
        organization_id=ORGANIZATION_ID,
        candidate=candidate,
        exclude_id=ENTRY_ID,
    )


# ============================================================
# Create
# ============================================================


def test_create_persists_a_valid_open_window_and_records_activity(mocker):
    active_organization(mocker)

    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=[],
    )

    created_entry = entry()

    create = mocker.patch.object(
        service.queries,
        "create_operating_hours",
        return_value=created_entry,
    )

    activity = mocker.patch.object(
        service,
        "_record_activity",
    )

    result = service.create_operating_hours(
        organization_id=ORGANIZATION_ID,
        payload=OperatingHoursCreate(
            day_of_week=0,
            slot_index=0,
            opens_at=time(8),
            closes_at=time(16),
        ),
        actor_id=USER_ID,
    )

    assert str(result.id) == ENTRY_ID

    payload = create.call_args.args[0]

    assert payload["organization_id"] == str(ORGANIZATION_ID)
    assert payload["created_by"] == str(USER_ID)
    assert payload["updated_by"] == str(USER_ID)

    activity.assert_called_once_with(
        action="operating_hours.created",
        event_type=service.EventTypes.OPERATING_HOURS_CREATED,
        entry=created_entry,
        actor_id=USER_ID,
    )


def test_create_allows_a_valid_split_shift(mocker):
    active_organization(mocker)

    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=[
            entry(
                slot_index=0,
                opens_at="08:00:00",
                closes_at="12:00:00",
            )
        ],
    )

    create = mocker.patch.object(
        service.queries,
        "create_operating_hours",
        return_value=entry(
            slot_index=1,
            opens_at="13:00:00",
            closes_at="17:00:00",
        ),
    )

    mocker.patch.object(service, "_record_activity")

    result = service.create_operating_hours(
        organization_id=ORGANIZATION_ID,
        payload=OperatingHoursCreate(
            day_of_week=0,
            slot_index=1,
            opens_at=time(13),
            closes_at=time(17),
        ),
        actor_id=USER_ID,
    )

    assert result.slot_index == 1
    create.assert_called_once()


def test_create_allows_closed_day(mocker):
    active_organization(mocker)

    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=[],
    )

    create = mocker.patch.object(
        service.queries,
        "create_operating_hours",
        return_value=entry(
            is_closed=True,
            opens_at=None,
            closes_at=None,
        ),
    )

    mocker.patch.object(service, "_record_activity")

    result = service.create_operating_hours(
        organization_id=ORGANIZATION_ID,
        payload=OperatingHoursCreate(
            day_of_week=6,
            is_closed=True,
        ),
        actor_id=USER_ID,
    )

    assert result.is_closed is True
    assert result.opens_at is None
    assert result.closes_at is None

    create.assert_called_once()


def test_create_rejects_an_overlapping_window(mocker):
    active_organization(mocker)

    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=[
            entry(
                opens_at="09:00:00",
                closes_at="17:00:00",
            )
        ],
    )

    with pytest.raises(OperatingHoursConflictError):
        service.create_operating_hours(
            organization_id=ORGANIZATION_ID,
            payload=OperatingHoursCreate(
                day_of_week=0,
                slot_index=1,
                opens_at=time(8),
                closes_at=time(10),
            ),
            actor_id=USER_ID,
        )


def test_create_rejects_duplicate_slot_index(mocker):
    active_organization(mocker)

    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=[
            entry(
                slot_index=0,
                opens_at="08:00:00",
                closes_at="10:00:00",
            )
        ],
    )

    with pytest.raises(OperatingHoursConflictError):
        service.create_operating_hours(
            organization_id=ORGANIZATION_ID,
            payload=OperatingHoursCreate(
                day_of_week=0,
                slot_index=0,
                opens_at=time(11),
                closes_at=time(12),
            ),
            actor_id=USER_ID,
        )


def test_create_rejects_closed_marker_when_windows_exist(mocker):
    active_organization(mocker)

    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=[entry()],
    )

    with pytest.raises(OperatingHoursConflictError):
        service.create_operating_hours(
            organization_id=ORGANIZATION_ID,
            payload=OperatingHoursCreate(
                day_of_week=0,
                slot_index=1,
                is_closed=True,
            ),
            actor_id=USER_ID,
        )


def test_create_rejects_missing_organization(mocker):
    mocker.patch.object(
        service.organization_queries,
        "get_organization",
        return_value=None,
    )

    with pytest.raises(OrganizationNotFoundError):
        service.create_operating_hours(
            organization_id=ORGANIZATION_ID,
            payload=OperatingHoursCreate(
                day_of_week=0,
                opens_at=time(8),
                closes_at=time(16),
            ),
            actor_id=USER_ID,
        )


def test_create_rejects_inactive_organization(mocker):
    inactive_organization(mocker)

    with pytest.raises(OrganizationInactiveError):
        service.create_operating_hours(
            organization_id=ORGANIZATION_ID,
            payload=OperatingHoursCreate(
                day_of_week=0,
                opens_at=time(8),
                closes_at=time(16),
            ),
            actor_id=USER_ID,
        )


# ============================================================
# Get / List
# ============================================================


def test_get_operating_hours_returns_entry(mocker):
    mocker.patch.object(
        service.queries,
        "get_operating_hours",
        return_value=entry(),
    )

    result = service.get_operating_hours(
        organization_id=ORGANIZATION_ID,
        operating_hours_id=ENTRY_ID,
    )

    assert str(result.id) == ENTRY_ID
    assert result.day_of_week == 0


def test_get_operating_hours_raises_when_missing(mocker):
    mocker.patch.object(
        service.queries,
        "get_operating_hours",
        return_value=None,
    )

    with pytest.raises(OperatingHoursNotFoundError):
        service.get_operating_hours(
            organization_id=ORGANIZATION_ID,
            operating_hours_id=ENTRY_ID,
        )


def test_list_operating_hours_validates_organization(mocker):
    active_organization(mocker)

    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=[entry()],
    )

    result = service.list_operating_hours(
        organization_id=ORGANIZATION_ID,
    )

    assert len(result) == 1
    assert str(result[0].id) == ENTRY_ID


def test_list_operating_hours_rejects_missing_organization(mocker):
    mocker.patch.object(
        service.organization_queries,
        "get_organization",
        return_value=None,
    )

    with pytest.raises(OrganizationNotFoundError):
        service.list_operating_hours(
            organization_id=ORGANIZATION_ID,
        )


def test_list_operating_hours_rejects_inactive_organization(mocker):
    inactive_organization(mocker)

    with pytest.raises(OrganizationInactiveError):
        service.list_operating_hours(
            organization_id=ORGANIZATION_ID,
        )


def test_list_operating_hours_returns_multiple_slots_in_order(mocker):
    active_organization(mocker)

    entries = [
        entry(
            slot_index=0,
            opens_at="08:00:00",
            closes_at="12:00:00",
        ),
        entry(
            id=SECOND_ENTRY_ID,
            slot_index=1,
            opens_at="13:00:00",
            closes_at="17:00:00",
        ),
    ]

    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=entries,
    )

    result = service.list_operating_hours(
        organization_id=ORGANIZATION_ID,
    )

    assert len(result) == 2
    assert result[0].slot_index == 0
    assert result[1].slot_index == 1


# ============================================================
# Update
# ============================================================


def test_update_validates_the_complete_merged_window(mocker):
    active_organization(mocker)

    mocker.patch.object(
        service.queries,
        "get_operating_hours",
        return_value=entry(),
    )

    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=[],
    )

    update = mocker.patch.object(
        service.queries,
        "update_operating_hours",
        return_value=entry(closes_at="18:00:00"),
    )

    mocker.patch.object(
        service,
        "_record_activity",
    )

    result = service.update_operating_hours(
        organization_id=ORGANIZATION_ID,
        operating_hours_id=ENTRY_ID,
        payload=OperatingHoursUpdate(
            closes_at=time(18),
        ),
        actor_id=USER_ID,
    )

    assert result.closes_at == time(18)
    assert update.call_args.args[2]["closes_at"] == "18:00:00"


def test_update_rejects_resulting_overlap(mocker):
    active_organization(mocker)

    mocker.patch.object(
        service.queries,
        "get_operating_hours",
        return_value=entry(
            slot_index=0,
            opens_at="08:00:00",
            closes_at="12:00:00",
        ),
    )

    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=[
            entry(
                id=SECOND_ENTRY_ID,
                slot_index=1,
                opens_at="13:00:00",
                closes_at="17:00:00",
            )
        ],
    )

    with pytest.raises(OperatingHoursConflictError):
        service.update_operating_hours(
            organization_id=ORGANIZATION_ID,
            operating_hours_id=ENTRY_ID,
            payload=OperatingHoursUpdate(
                closes_at=time(14),
            ),
            actor_id=USER_ID,
        )


def test_update_rejects_duplicate_slot_index(mocker):
    active_organization(mocker)

    mocker.patch.object(
        service.queries,
        "get_operating_hours",
        return_value=entry(slot_index=0),
    )

    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=[
            entry(
                id=SECOND_ENTRY_ID,
                slot_index=1,
                opens_at="13:00:00",
                closes_at="17:00:00",
            )
        ],
    )

    with pytest.raises(OperatingHoursConflictError):
        service.update_operating_hours(
            organization_id=ORGANIZATION_ID,
            operating_hours_id=ENTRY_ID,
            payload=OperatingHoursUpdate(
                slot_index=1,
            ),
            actor_id=USER_ID,
        )


def test_update_allows_adjacent_resulting_window(mocker):
    active_organization(mocker)

    mocker.patch.object(
        service.queries,
        "get_operating_hours",
        return_value=entry(
            slot_index=0,
            opens_at="08:00:00",
            closes_at="12:00:00",
        ),
    )

    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=[
            entry(
                id=SECOND_ENTRY_ID,
                slot_index=1,
                opens_at="13:00:00",
                closes_at="17:00:00",
            )
        ],
    )

    update = mocker.patch.object(
        service.queries,
        "update_operating_hours",
        return_value=entry(
            closes_at="13:00:00",
        ),
    )

    mocker.patch.object(service, "_record_activity")

    result = service.update_operating_hours(
        organization_id=ORGANIZATION_ID,
        operating_hours_id=ENTRY_ID,
        payload=OperatingHoursUpdate(
            closes_at=time(13),
        ),
        actor_id=USER_ID,
    )

    assert result.closes_at == time(13)
    update.assert_called_once()


def test_update_can_change_day(mocker):
    active_organization(mocker)

    mocker.patch.object(
        service.queries,
        "get_operating_hours",
        return_value=entry(day_of_week=0),
    )

    mocker.patch.object(
        service.queries,
        "list_operating_hours",
        return_value=[],
    )

    update = mocker.patch.object(
        service.queries,
        "update_operating_hours",
        return_value=entry(day_of_week=1),
    )

    mocker.patch.object(service, "_record_activity")

    result = service.update_operating_hours(
        organization_id=ORGANIZATION_ID,
        operating_hours_id=ENTRY_ID,
        payload=OperatingHoursUpdate(
            day_of_week=1,
        ),
        actor_id=USER_ID,
    )

    assert result.day_of_week == 1
    assert update.call_args.args[2]["day_of_week"] == 1


def test_update_rejects_missing_entry(mocker):
    active_organization(mocker)

    mocker.patch.object(
        service.queries,
        "get_operating_hours",
        return_value=None,
    )

    with pytest.raises(OperatingHoursNotFoundError):
        service.update_operating_hours(
            organization_id=ORGANIZATION_ID,
            operating_hours_id=ENTRY_ID,
            payload=OperatingHoursUpdate(
                closes_at=time(18),
            ),
            actor_id=USER_ID,
        )


# ============================================================
# Delete
# ============================================================


def test_delete_soft_deletes_and_records_activity(mocker):
    active_organization(mocker)

    mocker.patch.object(
        service.queries,
        "get_operating_hours",
        return_value=entry(),
    )

    deleted = entry(
        deleted_at=datetime.now(timezone.utc).isoformat(),
    )

    remove = mocker.patch.object(
        service.queries,
        "soft_delete_operating_hours",
        return_value=deleted,
    )

    activity = mocker.patch.object(
        service,
        "_record_activity",
    )

    service.delete_operating_hours(
        organization_id=ORGANIZATION_ID,
        operating_hours_id=ENTRY_ID,
        actor_id=USER_ID,
    )

    updates = remove.call_args.args[2]

    assert "deleted_at" in updates
    assert "updated_at" in updates
    assert updates["updated_by"] == str(USER_ID)

    activity.assert_called_once_with(
        action="operating_hours.deleted",
        event_type=service.EventTypes.OPERATING_HOURS_DELETED,
        entry=deleted,
        actor_id=USER_ID,
    )


def test_delete_rejects_missing_entry(mocker):
    active_organization(mocker)

    mocker.patch.object(
        service.queries,
        "get_operating_hours",
        return_value=None,
    )

    with pytest.raises(OperatingHoursNotFoundError):
        service.delete_operating_hours(
            organization_id=ORGANIZATION_ID,
            operating_hours_id=ENTRY_ID,
            actor_id=USER_ID,
        )


def test_delete_rejects_inactive_organization(mocker):
    inactive_organization(mocker)

    with pytest.raises(OrganizationInactiveError):
        service.delete_operating_hours(
            organization_id=ORGANIZATION_ID,
            operating_hours_id=ENTRY_ID,
            actor_id=USER_ID,
        )