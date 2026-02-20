from app.core.supabase import supabase
from fastapi import HTTPException
import uuid


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

    # Create Organization
    org_response = (
        supabase
        .table("organizations")
        .insert({
            "name": payload.name,
            "type": payload.type,
            "email": payload.email,
            "phone": payload.phone,
            "address": payload.address,
            "state": payload.state,
            "country": payload.country
        })
        .execute()
    )

    organization = org_response.data[0]

    # Insert Admin Record
    supabase.table("admins").insert({
        "id": admin_id,
        "organization_id": organization["id"],
        "role": "org_admin"
    }).execute()

    return {
        "message": "Organization registered successfully",
        "organization_id": organization["id"]
    }