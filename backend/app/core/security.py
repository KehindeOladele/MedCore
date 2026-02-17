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
) -> dict:
    """
    Validate Supabase JWT. Return the current user (id, email) and role (patient, doctor, clinician). 
    Reusable across all modules. Uses Supabase Tables as source of truth.
    
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
    
    # ----- Extract Role from User Metadata -----
    # firstly, try to get role from user_roles table
    role_query = (
    supabase
    .table("user_roles")
    .select("roles(name)")
    .eq("user_id", user.id)
    .single()
    .execute()
    )

    # secondly, if no role found in user_roles table, check user metadata
    if not role_query.data:
        raise HTTPException(
            status_code=403,
            detail="User role not configured"
        )
    
    # finally, assign role
    role = role_query.data["roles"]["name"]
    
    # print("USER METADATA:", user.user_metadata) # Debugging line to check user metadata

    # ----- Return User Information  from supabase instance -----
    return {
        "id": user.id,
        "email": user.email,
        "role": role,
    }
  

# ----- Role-Based Access Control -----
def require_role(required_role: str) -> callable:
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


# ----- Patient Access Dependency -----
def require_patient_access(patient_id: str, current_user: dict) -> None:
    """
    Enforce patient access rules:
    - Patient can access self
    - Clinician must be assigned via care_teams
    """
    role = current_user["role"]
    user_id = current_user["id"]

    # Patient accessing own record
    if role == "patient":
        if str(user_id) != str(patient_id):
            raise HTTPException(status_code=403, detail="Access denied")
        return

    # Clinicians must be assigned
    assign = (
        supabase
        .table("clinicians_patients")
        .select("clinician_id")
        .eq("clinician_id", user_id)
        .eq("patient_id", patient_id)
        .eq("active", True)
        .execute()
        .data
    )

    if not assign:
        raise HTTPException(status_code=403, detail="Patient not assigned")