from fastapi import APIRouter, Depends, UploadFile, File
from app.modules.organizations.models import (
    OrganizationCreate,
    OrganizationUpdate
)
from app.modules.organizations.service import create_organization
from app.core.dependencies import get_current_user
from app.core.supabase import supabase


# ----- Router Setup -----
router = APIRouter(prefix="/organizations", tags=["Organizations"])


#  ----- Organization Registration Endpoint -----
@router.post("/register")
def register_organization(payload: OrganizationCreate):
    return create_organization(payload)


# ----- Get My Organization Endpoint ----- 
@router.get("/me")
def get_my_organization(current_user=Depends(get_current_user)):

    response = (
        supabase
        .table("admins")
        .select("organization_id")
        .eq("id", current_user["id"])
        .single()
        .execute()
    )

    org_id = response.data["organization_id"]

    org = (
        supabase
        .table("organizations")
        .select("*")
        .eq("id", org_id)
        .single()
        .execute()
    )

    return org.data