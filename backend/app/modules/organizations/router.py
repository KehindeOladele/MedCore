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