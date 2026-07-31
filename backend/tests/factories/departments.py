def department_factory(**overrides):
    data = {
        "id": "dept-1",
        "organization_id": "org-1",
        "name": "Cardiology",
        "code": "CARD",
        "description": "Cardiology Department",
        "parent_department_id": None,
        "active": True,
        "created_at": "2026-07-30T12:00:00Z",
        "updated_at": "2026-07-30T12:00:00Z",
    }

    data.update(overrides)
    return data