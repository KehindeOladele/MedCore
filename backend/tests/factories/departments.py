from datetime import datetime, timezone
from uuid import uuid4


def department_factory(**overrides):
    now = datetime.now(timezone.utc)

    data = {
        "id": uuid4(),
        "organization_id": uuid4(),

        "name": "Cardiology",
        "code": "CARD",
        "description": "Cardiology Department",

        "parent_department_id": None,
        "active": True,

        "created_by": uuid4(),
        "updated_by": uuid4(),

        "created_at": now,
        "updated_at": now,
        "deleted_at": None,
    }

    data.update(overrides)

    return data