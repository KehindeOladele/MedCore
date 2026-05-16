from app.core.supabase_client import supabase
from fastapi import HTTPException
import uuid
from datetime import datetime, timedelta


#  ----- Organization Service -----
def create_organization(payload):

    # Create admin user in Supabase Auth
    auth_response = supabase.auth.admin.create_user({
        "email": payload.admin_email,
        "password": payload.admin_password,
        "email_confirm": True
    })

    if not auth_response.user:
        raise HTTPException(400, "Failed to create admin user")

    admin_id = auth_response.user.id

    # ----- Create Organization -----
    org_response = (
        supabase
        .table("organizations")
        .insert(payload.model_dump(exclude={"admin_email", "admin_password"}))
        .execute()
    )

    if not org_response.data:
        raise Exception("Failed to create organization")

    org = org_response.data[0]
    org_id = org["id"]

    # ----- Create Default Roles for Org -----
    default_roles = ["org_admin", "practitioner", "staff"]

    # Insert Default Roles
    roles_to_insert = [
        {
            "name": role,
            "organization_id": org_id,
            "role_type": "organization"
        }
        for role in default_roles
    ]

    supabase.table("roles").insert(roles_to_insert).execute()

    # Get org_admin role id
    role_resp = (
        supabase
        .table("roles")
        .select("id")
        .eq("name", "org_admin")
        .eq("organization_id", org_id)
        .single()
        .execute()
    )

    if not role_resp.data:
        raise Exception("org_admin role not found")

    role_id = role_resp.data["id"]

    # Assign role to admin
    supabase.table("user_roles").insert({
        "user_id": admin_id,
        "role_id": role_id,
        "organization_id": org_id
    }).execute()

    return {
        "message": "Organization registered successfully",
        "organization_id": org_id
    }


# ---- Update Organization Service -----
def update_organization(org_id: str, payload):

    update_data = payload.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided")

    response = (
        supabase
        .table("organizations")
        .update(update_data)
        .eq("id", org_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Organization not found")

    return response.data[0]


# ---- Role Management Service -----
def assign_user_role(role_data: dict):

    # ---- Get Role ID ----
    role_resp = (
    supabase
    .table("roles")
    .select("id")
    .eq("name", role_data["role_name"])
    .eq("organization_id", role_data["org_id"])
    .single()
    .execute()
)

    if not role_resp.data:
        raise Exception("Role not found")

    role_id= role_resp.data[0]["id"]

    # ---- Insert Mapping ----
    result = (
        supabase
        .table("user_roles")
        .upsert({
            "user_id": role_data["user_id"],
            "role_id": role_id,
            "organization_id": role_data["org_id"]
        })
        .execute()
    )

    if not result.data:
        raise Exception("Failed to assign role")

    return result.data[0]


# ---- Onboarding Invite Service -----
def create_invitation(org_id: str, email: str, role_name: str, invited_by: str):

    token = str(uuid.uuid4())

    result = (
        supabase
        .table("invitations")
        .insert({
            "email": email,
            "organization_id": org_id,
            "role_name": role_name,
            "invited_by": invited_by,
            "token": token,
            "expires_at": (datetime.utcnow() + timedelta(days=2)).isoformat()
        })
        .execute()
    )

    if not result.data:
        raise Exception("Failed to create invitation")

    # TODO: send email with token link
    # link = f"https://your-frontend.com/accept-invite?token={token}"

    return result.data[0]


# ----- Accept Invitation Service -----
def accept_invitation(payload: dict):

    # ---- Find invitation ----
    invite_resp = (
        supabase
        .table("invitations")
        .select("*")
        .eq("token", payload["token"])
        .eq("status", "pending")
        .single()
        .execute()
    )

    if not invite_resp.data:
        raise Exception("Invalid or expired invitation")

    invite = invite_resp.data

    if datetime.now() > datetime.fromisoformat(invite["expires_at"]):
        raise Exception("Invitation expired")

    # ---- Create user in Supabase Auth ----
    res = supabase.auth.sign_up({
        "email": invite["email"],
        "password": payload["password"]
    })

    user = res.user

    if not user:
        raise Exception("Signup failed")

    # ---- Assign role ----
    role_resp = (
        supabase
        .table("roles")
        .select("id")
        .eq("name", invite["role_name"])
        .eq("organization_id", invite["organization_id"])
        .single()
        .execute()
    )

    if not role_resp.data:
        raise Exception("Role not found")

    role_id = role_resp.data["id"]

    supabase.table("user_roles").insert({
        "user_id": user.id,
        "role_id": role_id,
        "organization_id": invite["organization_id"]
    }).execute()

    # ---- Mark invitation accepted ----
    supabase.table("invitations").update({
        "status": "accepted"
    }).eq("id", invite["id"]).execute()

    return {
        "message": "Account created successfully",
        "user_id": user.id
    }