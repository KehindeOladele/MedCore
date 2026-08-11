from copy import deepcopy

from .constants import (
ORGANIZATION_ID,
HEALTHCARE_SERVICE_ID,
USER_ID
)

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


_DEFAULT_HEALTHCARE_SERVICE_ROW= {
        "id": HEALTHCARE_SERVICE_ID,
        "organization_id": ORGANIZATION_ID,
        "name": "Cardiology",
        "code": "CARD",
        "description": "Cardiology services",
        "category": "Specialty",
        "type": "Clinical",
        "specialty": "Cardiology",
        "phone": "08012345678",
        "email": "cardiology@test.com",
        "website": "https://hospital.test/cardiology",
        "appointment_required": True,
        "referral_required": False,
        "online_booking_available": True,
        "department_id": None,
        "service_code": None,
        "display_order": 1,
        "active": True,
        "created_by": USER_ID,
        "updated_by": USER_ID,
        "created_at": "2026-08-01T10:00:00Z",
        "updated_at": "2026-08-01T10:00:00Z",
    }


# --------------------------------------
# ORGANIZATION LAYER
# --------------------------------------
def organization_factory(**overrides):
    row = organization_row_factory(**overrides)
    return {
        "id": row["id"],
        "name": row["name"],
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
        "id": str(row["id"]),
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



# --------------------------------------
# HEALTHCARE SERVICE LAYER (FLAT ROWS)
# --------------------------------------
def healthcare_service_row_factory(**overrides):
    healthcare_service = deepcopy(_DEFAULT_HEALTHCARE_SERVICE_ROW)
    healthcare_service.update(overrides)
    return healthcare_service