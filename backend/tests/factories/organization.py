from copy import deepcopy
from uuid import uuid4


ORGANIZATION_ID = uuid4()
OTHER_ORGANIZATION_ID = uuid4()


_DEFAULT_ORGANIZATION_ROW = {
    "id": ORGANIZATION_ID,
    "active": True,
    "name": "Test Hospital",
    "type": "hospital",
    "phone": "08012345678",
    "email": "admin@test.com",
    "website": "https://hospital.test",
    "address": "123 Main Street",
    "city": "Lagos",
    "state": "Lagos",
    "postal_code": "100001",
    "country": "Nigeria",
    "description": None,
    "logo_url": None,
    "timezone": "Africa/Lagos",
    "setup_completed": False,
}



# --------------------------------------
# ORGANIZATION LAYER
# --------------------------------------
def organization_factory(**overrides):
    row = organization_row_factory(**overrides)
    return {
        "id": row["id"],
        "name": row["address"],
        "type": row["type"],
        "active": True,
    }

# --------------------------------------
# SERVICE LAYER (FLAT ROWS)
# --------------------------------------
def organization_row_factory(**overrides):
    organization = deepcopy(_DEFAULT_ORGANIZATION_ROW)
    organization.update(overrides)
    return organization


# --------------------------------------
# ROUTER LAYER (NESTED API ROWS)
# --------------------------------------
def organization_profile_factory(**overrides):
    row = organization_row_factory(**overrides)

    return {
        "id": row["id"],
        "active": row["active"],
        "name": row["name"],
        "type": row["type"],
        "telecom": {
            "phone": row.get("phone"),
            "email": row.get("email"),
            "website": row.get("website"),
        },
        "address": {
            "line": row.get("address"),
            "city": row.get("city"),
            "state": row.get("state"),
            "postal_code": row.get("postal_code"),
            "country": row.get("country"),
        },
        "description": row.get("description"),
        "logo_url": row.get("logo_url"),
        "timezone": row.get("timezone"),
        "setup_completed": row.get("setup_completed", False),
    }