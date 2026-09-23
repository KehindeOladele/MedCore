from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from app.core.security import get_current_user

from app.modules.organizations.dependencies import (
    require_organization_admin,
    require_organization_access,
)

from .schemas import (
    HealthcareServiceCreate,
    HealthcareServiceUpdate,
    HealthcareServiceResponse,
)

from .service import (
    create_healthcare_service,
    get_healthcare_service,
    list_healthcare_services,
    update_healthcare_service,
    delete_healthcare_service,
)


# -------------------------------------------------------
# HEALTHCARE SERVICE API SETUP
# -------------------------------------------------------

router = APIRouter(
    prefix="/{organization_id}/healthcare-services",
    tags=["Healthcare Services"],
)


# -------------------------------------------------------
# CREATE HEALTHCARE SERVICE ENDPOINT
# -------------------------------------------------------

@router.post(
    "",
    response_model=HealthcareServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_healthcare_service_endpoint(
    organization_id: UUID,
    payload: HealthcareServiceCreate,
    current_user=Depends(get_current_user),
    organization=Depends(require_organization_admin),
):
    return create_healthcare_service(
        organization_id=organization_id,
        payload=payload,
        actor_id=current_user["id"],
    )


# -------------------------------------------------------
# LIST HEALTHCARE SERVICES ENDPOINT
# -------------------------------------------------------

@router.get(
    "",
    response_model=list[HealthcareServiceResponse],
)
def list_healthcare_services_endpoint(
    organization_id: UUID,
    current_user=Depends(get_current_user),
    organization=Depends(require_organization_access),
):
    return list_healthcare_services(
        organization_id=organization_id,
    )


# -------------------------------------------------------
# GET HEALTHCARE SERVICE ENDPOINT
# -------------------------------------------------------

@router.get(
    "/{healthcare_service_id}",
    response_model=HealthcareServiceResponse,
)
def get_healthcare_service_endpoint(
    organization_id: UUID,
    healthcare_service_id: UUID,
    current_user=Depends(get_current_user),
    organization=Depends(require_organization_access),
):
    return get_healthcare_service(
        organization_id=organization_id,
        healthcare_service_id=healthcare_service_id,
    )


# -------------------------------------------------------
# UPDATE HEALTHCARE SERVICE ENDPOINT
# -------------------------------------------------------

@router.patch(
    "/{healthcare_service_id}",
    response_model=HealthcareServiceResponse,
)
def update_healthcare_service_endpoint(
    organization_id: UUID,
    healthcare_service_id: UUID,
    payload: HealthcareServiceUpdate,
    current_user=Depends(get_current_user),
    organization=Depends(require_organization_admin),
):
    return update_healthcare_service(
        organization_id=organization_id,
        healthcare_service_id=healthcare_service_id,
        payload=payload,
        actor_id=current_user["id"],
    )


# -------------------------------------------------------
# DELETE HEALTHCARE SERVICE ENDPOINT
# -------------------------------------------------------

@router.delete(
    "/{healthcare_service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_healthcare_service_endpoint(
    organization_id: UUID,
    healthcare_service_id: UUID,
    current_user=Depends(get_current_user),
    organization=Depends(require_organization_admin),
):
    delete_healthcare_service(
        organization_id=organization_id,
        healthcare_service_id=healthcare_service_id,
        actor_id=current_user["id"],
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )