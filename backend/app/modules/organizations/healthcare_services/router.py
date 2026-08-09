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
    require_organization_access
)

from .schemas import (
    HealthcareServiceCreate,
    HealthcareServiceUpdate,
    HealthcareServiceResponse,
)

from app.modules.organizations.healthcare_services.service import (
    create_healthcare_service,
    get_healthcare_service,
    list_healthcare_services,
    update_healthcare_service,
    delete_healthcare_service,
)




# -------------------------------------------------------
# HEALTHCARE SERVIVE API SETUP
# -------------------------------------------------------
router = APIRouter(
    prefix="/healthcare-services",
    tags=["Healthcare Services"],
)



# -------------------------------------------------------
# CREATE HEALTHCARE SERVICE ENDPOINT
# -------------------------------------------------------
@router.post(
    "/",
    response_model=HealthcareServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_healthcare_service_endpoint(
    payload: HealthcareServiceCreate,
    current_user=Depends(get_current_user),
    _: dict = Depends(require_organization_admin),
):
    return create_healthcare_service(
        organization_id=current_user["organization_id"],
        payload=payload,
        actor_id=current_user["id"],
    )


# -------------------------------------------------------
# LIST HEALTHCARE SERVICE ENDPOINT
# -------------------------------------------------------
@router.get(
    "/",
    response_model=list[HealthcareServiceResponse],
)
def list_healthcare_services_endpoint(
    current_user=Depends(get_current_user),
    _: dict = Depends(require_organization_access),
):
    return list_healthcare_services(
        organization_id=current_user["organization_id"],
    )


# -------------------------------------------------------
# GET HEALTHCARE SERVICE ENDPOINT
# -------------------------------------------------------
@router.get(
    "/{healthcare_service_id}",
    response_model=HealthcareServiceResponse,
)
def get_healthcare_service_endpoint(
    healthcare_service_id: UUID,
    current_user=Depends(get_current_user),
    _: dict = Depends(require_organization_access),
):
    return get_healthcare_service(
        organization_id=current_user["organization_id"],
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
    healthcare_service_id: UUID,
    payload: HealthcareServiceUpdate,
    current_user=Depends(get_current_user),
    _: dict = Depends(require_organization_admin),
):
    return update_healthcare_service(
        organization_id=current_user["organization_id"],
        healthcare_service_id=healthcare_service_id,
        payload=payload,
        actor_id=current_user["id"],
    )


# -------------------------------------------------------
# UPDATE HEALTHCARE SERVICE ENDPOINT
# -------------------------------------------------------
@router.delete(
    "/{healthcare_service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_healthcare_service_endpoint(
    healthcare_service_id: UUID,
    current_user=Depends(get_current_user),
    _: dict = Depends(require_organization_admin),
):
    delete_healthcare_service(
        organization_id=current_user["organization_id"],
        healthcare_service_id=healthcare_service_id,
        actor_id=current_user["id"],
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)