from app.core.events.emitter import emit_event
from app.core.events.schemas import EventTypes


# ----- Event Service Layer ----- 
class EventService:
    @staticmethod
    def patient_created(
        patient_id: str,
        email: str | None
    ):
        emit_event(
            aggregate_type="patient",
            aggregate_id=patient_id,
            event_type=EventTypes.PATIENT_CREATED,
            payload={
                "email": email
            }
        )