# modules/dashboard/router.py

from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from .service import build_user_summary

router = APIRouter(prefix="/api/v1", tags=["Dashboard"])

# This endpoint provides a summary of the user's health data, 
# including their profile information, active prescriptions, 
# and upcoming reminders. 
@router.get("/user/summary")
def user_summary(current_user=Depends(get_current_user)):
    return build_user_summary(current_user)
