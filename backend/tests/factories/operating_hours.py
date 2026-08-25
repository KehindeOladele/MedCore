from copy import deepcopy

from .constants import (
ORGANIZATION_ID,
USER_ID,
OPERATING_HOURS_ID
)



def response_data(**overrides):
    data = {
        "id": str(OPERATING_HOURS_ID),
        "organization_id": str(ORGANIZATION_ID),
        "day_of_week": 0,
        "slot_index": 0,
        "opens_at": "08:00:00",
        "closes_at": "16:00:00",
        "is_closed": False,
        "created_by": str(USER_ID),
        "updated_by": str(USER_ID),
        "deleted_at": None,
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z",
    }

    data.update(overrides)
    return data