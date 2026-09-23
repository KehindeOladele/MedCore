from datetime import time

import pytest
from pydantic import ValidationError

from app.modules.organizations.operating_hours.schemas import OperatingHoursCreate, OperatingHoursUpdate


def test_open_window_requires_both_times():
    with pytest.raises(ValidationError, match="require opens_at"):
        OperatingHoursCreate(day_of_week=0, opens_at=time(8))


def test_open_window_requires_closing_after_opening():
    with pytest.raises(ValidationError, match="later than"):
        OperatingHoursCreate(day_of_week=0, opens_at=time(17), closes_at=time(8))


def test_closed_day_cannot_include_times():
    with pytest.raises(ValidationError, match="Closed days"):
        OperatingHoursCreate(day_of_week=6, is_closed=True, opens_at=time(8))


def test_valid_open_window():
    payload = OperatingHoursCreate(day_of_week=0, slot_index=1, opens_at=time(8), closes_at=time(16))
    assert payload.day_of_week == 0
    assert payload.slot_index == 1


def test_valid_closed_day():
    payload = OperatingHoursCreate(day_of_week=6, is_closed=True)
    assert payload.is_closed is True
    assert payload.opens_at is None


@pytest.mark.parametrize("day", [-1, 7])
def test_weekday_is_limited_to_iso_week(day):
    with pytest.raises(ValidationError):
        OperatingHoursCreate(day_of_week=day, opens_at=time(8), closes_at=time(16))


def test_update_is_partial():
    assert OperatingHoursUpdate(is_closed=True).model_dump(exclude_unset=True) == {"is_closed": True}
