from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.supabase_client import supabase
from app.core.supabase_admin import supabase_admin
# from jose import jwt 
# from jose.exceptions import JWTError
from app.core.config import settings
from app.core.rbac import has_permission
from fastapi import Depends, HTTPException
from app.modules.practitioners.service import (
    get_practitioner_by_id
)
from datetime import datetime, timezone


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

    # ----- Fetch ALL roles -----
    try:
        role_query = (
            supabase
            .table("user_roles")
            .select("roles(name)")
            .eq("user_id", user.id)
            .single()
            .execute()
        )
    except Exception:
        raise HTTPException(
            status_code=403,
            detail="User role not configured"
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
        "role": role,
        "roles": roles,
        "organization_ids": list(org_ids),
        "is_patient": is_patient,
        "is_practitioner": is_practitioner,
        "is_admin": is_admin,
        "is_super_admin": is_super_admin,
    }


# ----- Role-Based Access Control -----
def require_role(required_role: str) -> callable:
    """
    Check if the current user has the required systen role.

    input: required_role (str)
    Returns: function that raises HTTPException if role is insufficient
    """
    def checker(user=Depends(get_current_user)):

        roles_resp = (
            supabase
            .table("user_roles")
            .select("""
                role:roles(name, role_type)
            """)
            .eq("user_id", user["id"])
            .is_("organization_id", None)
            .execute()
        )

        role_names = [
            r["role"]["name"]
            for r in roles_resp.data
        ]

        if required_role not in role_names:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
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
def require_permission(permission_name: str, org_id_param: str = "org_id"):
    def checker(
        request: Request,
        current_user=Depends(get_current_user)
    ):
        user_id = current_user["id"]

        # ---- Extract org_id dynamically from path ----
        org_id = request.path_params.get(org_id_param)

        if not org_id:
            raise HTTPException(400, "Organization context required")

        result = (
            supabase
            .table("user_roles")
            .select("""
                organization_id,
                roles!inner(
                    name,
                    role_permissions!inner(
                        permissions!inner(name)
                    )
                )
            """)
            .eq("user_id", user_id)
            .eq("organization_id", org_id)
            .execute()
        )

        if not result.data:
            raise HTTPException(403, "No roles in this organization")

        permissions = set()

        for row in result.data:
            role = row.get("roles")
            if not role:
                continue

            for rp in role.get("role_permissions", []):
                perm = rp.get("permissions")
                if perm:
                    permissions.add(perm.get("name"))

        if permission_name not in permissions:
            raise HTTPException(403, "Permission denied")

        return current_user

    return checker


# ----- Patient Access Dependency -----
def require_patient_access():

    def checker(
        patient_id: str,
        organization_id: str,
        user=Depends(get_current_user)
    ):

        consent = (
            supabase
            .table("consent_records")
            .select("*")
            .eq("patient_id", patient_id)
            .eq("organization_id", organization_id)
            .eq("status", "active")
            .execute()
        )

        if consent.data:
            return user

        care_team = (
            supabase
            .table("patient_care_team")
            .select("*")
            .eq("patient_id", patient_id)
            .eq("practitioner_id", user["id"])
            .eq("organization_id", organization_id)
            .eq("status", "active")
            .execute()
        )

        if care_team.data:
            return user

        raise HTTPException(
            status_code=403,
            detail="Patient access denied"
        )

    return checker
    

# ----- Organization Role Authorization -----
def require_org_role(required_role: str):

    def checker(
        organization_id: str,
        user=Depends(get_current_user)
    ):

        role = (
            supabase
            .table("practitioner_roles")
            .select("*")
            .eq("practitioner_id", user["id"])
            .eq("organization_id", organization_id)
            .eq("role_code", required_role)
            .eq("active", True)
            .execute()
        )

        if not role.data:
            raise HTTPException(
                status_code=403,
                detail="Organization access denied"
            )

        return user

    return checker


# ----- Require Practitoners Authorization -----
def require_practitioner(
    user=Depends(get_current_user)
):

    practitioner = get_practitioner_by_id(
        user["id"]
    )

    if not practitioner:
        raise HTTPException(
            status_code=403,
            detail="Practitioner account required"
        )

    return practitioner


# ----- Organization Role Authorization -----
def require_org_role(
    organization_id: str,
    allowed_roles: list[str] | None = None
):

    def dependency(
        practitioner=Depends(require_practitioner)
    ):

        query = (
            supabase_admin
            .table("practitioner_roles")
            .select("*")
            .eq("practitioner_id", practitioner["id"])
            .eq("organization_id", organization_id)
            .eq("active", True)
        )

        if allowed_roles:
            query = query.in_(
                "role_code",
                allowed_roles
            )

        response = query.execute()

        if not response.data:
            raise HTTPException(
                status_code=403,
                detail="Organization access denied"
            )

        return response.data[0]

    return dependency


# ----- Patient Access Authorizaton for Practitioners-----
def require_patient_access():

    def dependency(
        patient_id: str,
        organization_id: str,
        practitioner=Depends(require_practitioner)
    ):

        now = datetime.now(
            timezone.utc
        ).isoformat()

        # CHECK FOR CARE TEAM ACCESS
        care_team = (
            supabase_admin
            .table("patient_care_team")
            .select("*")
            .eq("patient_id", patient_id)
            .eq("organization_id", organization_id)
            .eq("practitioner_id", practitioner["id"])
            .eq("active", True)
            .execute()
        )

        if care_team.data:
            return practitioner

        # CHECK FOR CONSENT ACCESS
        consent = (
            supabase_admin
            .table("consent_records")
            .select("*")
            .eq("patient_id", patient_id)
            .eq("organization_id", organization_id)
            .eq("status", "active")
            .or_(
                f"""
                practitioner_id.eq.{practitioner["id"]},
                practitioner_id.is.null
                """
            )
            .execute()
        )

        if not consent.data:
            raise HTTPException(
                status_code=403,
                detail="Patient access denied"
            )

        valid_consents = []

        for item in consent.data:

            if (
                item.get("expires_at")
                and item["expires_at"] < now
            ):
                continue

            valid_consents.append(item)

        if not valid_consents:
            raise HTTPException(
                status_code=403,
                detail="Consent expired"
            )

        return practitioner

    return dependency