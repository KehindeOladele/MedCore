from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.core.security import get_current_user
from app.modules.organizations.dependencies import require_organization_access, require_organization_admin

from .schemas import OperatingHoursCreate, OperatingHoursResponse, OperatingHoursUpdate
from .service import create_operating_hours, delete_operating_hours, get_operating_hours, list_operating_hours, update_operating_hours


router = APIRouter(prefix="/{organization_id}/operating-hours", tags=["Organization Operating Hours"])


@router.post("", response_model=OperatingHoursResponse, status_code=status.HTTP_201_CREATED)
def create_operating_hours_endpoint(organization_id: UUID, payload: OperatingHoursCreate, current_user=Depends(get_current_user), organization=Depends(require_organization_admin)):
    return create_operating_hours(organization_id=organization_id, payload=payload, actor_id=current_user["id"])


@router.get("", response_model=list[OperatingHoursResponse])
def list_operating_hours_endpoint(organization_id: UUID, current_user=Depends(get_current_user), organization=Depends(require_organization_access)):
    return list_operating_hours(organization_id=organization_id)


@router.get("/{operating_hours_id}", response_model=OperatingHoursResponse)
def get_operating_hours_endpoint(organization_id: UUID, operating_hours_id: UUID, current_user=Depends(get_current_user), organization=Depends(require_organization_access)):
    return get_operating_hours(organization_id=organization_id, operating_hours_id=operating_hours_id)


@router.patch("/{operating_hours_id}", response_model=OperatingHoursResponse)
def update_operating_hours_endpoint(organization_id: UUID, operating_hours_id: UUID, payload: OperatingHoursUpdate, current_user=Depends(get_current_user), organization=Depends(require_organization_admin)):
    return update_operating_hours(organization_id=organization_id, operating_hours_id=operating_hours_id, payload=payload, actor_id=current_user["id"])


@router.delete("/{operating_hours_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_operating_hours_endpoint(organization_id: UUID, operating_hours_id: UUID, current_user=Depends(get_current_user), organization=Depends(require_organization_admin)):
    delete_operating_hours(organization_id=organization_id, operating_hours_id=operating_hours_id, actor_id=current_user["id"])
    return Response(status_code=status.HTTP_204_NO_CONTENT)
