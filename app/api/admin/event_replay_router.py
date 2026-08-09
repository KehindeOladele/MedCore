from fastapi import (
    APIRouter,
    Depends
)
from app.core.security import (
    get_current_user
)
from app.core.events.replay import (
    replay_dead_event
)


router = APIRouter(
    prefix="/admin/events",
    tags=["Event Replay"]
)


# ---------------------
# REPLAY DEAD EVENT ENDPOINT
# ---------------------
@router.post(
    "/dead/{event_id}/replay"
)
def replay_event(
    event_id: str,
    user=Depends(
        get_current_user
    )
):
    return replay_dead_event(
        dead_event_id=event_id,
        actor_id=user["id"]
    )