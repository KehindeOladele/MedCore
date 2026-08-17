from copy import deepcopy

from .constants import (
ORGANIZATION_ID,
HEALTHCARE_SERVICE_ID,
USER_ID
)

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
# HEALTHCARE SERVICE LAYER (FLAT ROWS)
# --------------------------------------
def healthcare_service_row_factory(**overrides):
    healthcare_service = deepcopy(_DEFAULT_HEALTHCARE_SERVICE_ROW)
    healthcare_service.update(overrides)
    return healthcare_service