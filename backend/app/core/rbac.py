ROLE_PERMISSIONS = {
    "patient": [],
    "nurse": ["create_observation"],
    "clinician": ["create_observation"],
    "laboratory scientist": ["create_observation"],
    "doctor": [
        "create_observation",
        "create_condition",
        "create_medication"
    ],
    "admin": ["*"]
}


# ----- RBAC Utility Functions -----
def has_permission(user_role: str, permission: str) -> bool:
    if user_role == "admin":
        return True
    return permission in ROLE_PERMISSIONS.get(user_role, [])
