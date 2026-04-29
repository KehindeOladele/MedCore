from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.supabase_client import supabase
from jose import jwt  
from jose.exceptions import JWTError
from app.core.config import settings


# ----- Security Dependencies -----
security = HTTPBearer()


# ----- Get Current User -----
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Validate Supabase JWT. Return the current user (id, email, role). Reusable across all modules.
    Uses Supabase as source of truth. No JWT secret needed. ackend-enforced access
    
    inpt: HTTPAuthorizationCredentials from FastAPI's HTTPBearer
    Returns: dict with user info (id, email, role)
    """
    
    # ----- Verify Token and Retrieve User -----
    token = credentials.credentials # Extract token from credentials

    # ----- Verify Token with Supabase -----
    try:
        response = supabase.auth.get_user(token)
        user = response.user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    # ----- Check if User Exists -----
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )

    # ----- Fetch ALL roles -----
    role_query = (
        supabase
        .table("user_roles")
        .select("organization_id, roles(name, role_type)")
        .eq("user_id", user.id)
        .execute()
    )

    roles_data = role_query.data or []

    if not roles_data:
        raise HTTPException(
            status_code=403,
            detail="User has no assigned roles"
        )
    
    # ----- Normalize roles -----
    roles = []
    org_ids = set()

    for r in roles_data:
        role_name = r["roles"]["name"]
        role_type = r["roles"]["role_type"]
        org_id = r["organization_id"]

        roles.append({
            "name": role_name,
            "role_type": role_type,
            "organization_id": org_id
        })

        if org_id:
            org_ids.add(org_id)

    # ----- Derive flags (useful for frontend & permissions) -----
    is_patient = any(r["name"] == "patient" for r in roles)
    is_practitioner = any(r["name"] == "practitioner" for r in roles)
    is_admin = any(r["name"] == "org_admin" for r in roles)
    is_super_admin = any(r["role_type"] == "system" for r in roles)


    # ----- Return User Information  from supabase instance-----
    return {
        "id": user.id,
        "email": user.email,
        "roles": roles,
        "organization_ids": list(org_ids),
        "is_patient": is_patient,
        "is_practitioner": is_practitioner,
        "is_admin": is_admin,
        "is_super_admin": is_super_admin,
    }


# ----- Role-Based Access Control -----
def require_role(required_role: str):
    """
    Check if the current user has the required role.

    input: required_role (str)
    Returns: function that raises HTTPException if role is insufficient
    """
    def checker(user=Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user

    return checker