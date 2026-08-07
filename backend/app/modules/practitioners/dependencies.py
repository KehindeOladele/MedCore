from fastapi import Depends, HTTPException
from app.core.security import get_current_user
from app.modules.practitioners.service import (
    get_practitioner_by_id
)


# -----  Practitioners Services Helper -----
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