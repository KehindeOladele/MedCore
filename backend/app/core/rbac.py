# app/core/rbac.py
# ----- Role-Based Access Control (RBAC) -----
ROLE_PERMISSIONS = {
    "patient": [
        "read_own_records"
    ],

    "nurse": [
        "create_observation",
        "read_patient_records"
    ],

    "clinician": [
        "create_observation",
        "read_patient_records"
    ],

    "doctor": [
        "create_observation",
        "create_condition",
        "create_medication",
        "read_patient_records"
    ],

    "lab-tech": [
        "create_observation"
    ],

    "admin": ["*"]
}


# ----- Check if a role has a specific permission -----
def has_permission(role: str, permission: str) -> bool:
    if role == "admin":
        return True
    return permission in ROLE_PERMISSIONS.get(role, [])
