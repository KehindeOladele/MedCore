from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.supabase_client import supabase
from jose import jwt  
from jose.exceptions import JWTError
from app.core.config import settings
from app.core.rbac import has_permission


# ----- Security Dependencies -----
security = HTTPBearer()


# ----- Get Current User -----
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
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

    # ----- Return User Information  from supabase instance-----
    return {
        "id": user.id,
        "email": user.email,
        "role": user.user_metadata.get("role", "patient"),
    }


# ----- Role-Based Access Control -----
def require_role(required_role: str):
    """
    Check if the current user has the required role.

    input: required_role (str)
    Returns:ncy function that raises HTTPException if role is insufficient
    """
    def checker(user=Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user

    return checker


# ---- Get User Permissions -----
def get_user_permissions(user_id: str) -> set[str]:
    response = (
        supabase
        .rpc("get_user_permissions", {"uid": user_id})
        .execute()
    )

    return {p["permission"] for p in response.data}


# ----- Permission Guard Dependency -----
def require_permission(permission_name: str):
    def checker(current_user=Depends(get_current_user)):

        user_id = current_user["id"]

        result = (
            supabase
            .table("user_roles")
            .select(
                "roles!inner(id, name, role_permissions!inner(permissions!inner(name)))"
            )
            .eq("user_id", user_id)
            .execute()
        )

        if not result.data:
            raise HTTPException(403, "Not authorized")

        permissions = {
            perm["name"]
            for role in result.data
            for rp in role["roles"]["role_permissions"]
            for perm in [rp["permissions"]]
        }

        if permission_name not in permissions:
            raise HTTPException(403, "Not authorized")

        return current_user

    return checker
