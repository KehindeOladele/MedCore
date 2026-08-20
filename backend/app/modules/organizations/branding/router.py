from uuid import UUID

from fastapi import (
    APIRouter, 
    Depends, 
    File, 
    Response, 
    UploadFile, 
    status
)

from app.core.security import get_current_user
from app.modules.organizations.dependencies import (
    require_organization_access, 
    require_organization_admin
)
from .schemas import (
    BrandingResponse, 
    BrandingThemeUpdate
)

from .service import (
    get_organization_branding, 
    remove_logo, 
    update_theme, 
    upload_logo
)


router = APIRouter(prefix="/{organization_id}/branding", tags=["Organization Branding"])



# ====================================================================================
# ORGANIZATION BRANDING ENDPOINTS
# ====================================================================================

# -----------------------------------------------------------------------------------
# Get Organization Branding
# -----------------------------------------------------------------------------------
@router.get("", response_model=BrandingResponse)
def get_branding_endpoint(
    organization_id: UUID, 
    current_user=Depends(get_current_user), 
    organization=Depends(require_organization_access)
    ):

    return get_organization_branding(organization_id=organization_id)


# -----------------------------------------------------------------------------------
# Update Organization Branding Theme
# -----------------------------------------------------------------------------------
@router.put("/theme", response_model=BrandingResponse)
def update_theme_endpoint(
    organization_id: UUID, 
    payload: BrandingThemeUpdate, 
    current_user=Depends(get_current_user), 
    organization=Depends(require_organization_admin)
    ):

    return update_theme(organization_id=organization_id, payload=payload, actor_id=current_user["id"])


# -----------------------------------------------------------------------------------
# Upload Organization Logo
# -----------------------------------------------------------------------------------
@router.put("/logo", response_model=BrandingResponse)
async def upload_logo_endpoint(
    organization_id: UUID, 
    file: UploadFile = File(...), 
    current_user=Depends(get_current_user), 
    organization=Depends(require_organization_admin)
    ):

    return upload_logo(
        organization_id=organization_id, 
        content_type=file.content_type, 
        content=await file.read(), 
        actor_id=current_user["id"]
        )


# -----------------------------------------------------------------------------------
# Remove Organization Logo
# -----------------------------------------------------------------------------------
@router.delete("/logo", status_code=status.HTTP_204_NO_CONTENT)
def remove_logo_endpoint(
    organization_id: UUID, 
    current_user=Depends(get_current_user), 
    organization=Depends(require_organization_admin)
    ):

    remove_logo(organization_id=organization_id, actor_id=current_user["id"])

    return Response(status_code=status.HTTP_204_NO_CONTENT)
