from fastapi import APIRouter
from app.core.supabase_admin import supabase_admin

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

# ----- Admin Event Monitoring Endpoint -----
@router.get("/events")
def get_events():

    return (
        supabase_admin
        .table("events")
        .select("*")
        .order("created_at", desc=True)
        .limit(100)
        .execute()
        .data
    )