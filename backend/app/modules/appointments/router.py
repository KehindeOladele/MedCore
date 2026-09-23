from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from app.core.security import (
    get_current_user
)
from app.core.supabase_admin import (
    supabase_admin
)
from app.modules.appointments.schemas import (
    AppointmentCreate,
    AppointmentUpdate
)
from app.modules.appointments.service import (
    create_appointment,
    get_patient_appointments,
    get_practitioner_appointments,
    update_appointment
)
from app.modules.observations.dependencies import (
    require_patient_access_manual
)



# ----- Appointments Router Setup -----
router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


# ----- Create Appointment Endpoint -----
@router.post("/")
def create_new_appointment(
    payload: AppointmentCreate,
    user=Depends(get_current_user)
):

    require_patient_access_manual(
        patient_id=payload.patient_id,
        user_id=user["id"]
    )

    return create_appointment(
        payload=payload,
        created_by=user["id"]
    )



# ----- Get Patient Appointments Endpoint -----
@router.get("/patient/{patient_id}")
def get_appointments(
    patient_id: str,
    user=Depends(get_current_user)
):

    require_patient_access_manual(
        patient_id=patient_id,
        user_id=user["id"]
    )

    return get_patient_appointments(
        patient_id
    )



# ----- Get Practitioners Appointments Endpoint -----
@router.get("/practitioner/{practitioner_id}")
def request_practitioner_appointments(
    practitioner_id: str,
    user=Depends(get_current_user)
):

    return get_practitioner_appointments(
        practitioner_id
    )


# ----- Update Patients Appointment -----
@router.patch("/{appointment_id}")
def update_patient_appointment(
    appointment_id: str,
    payload: AppointmentUpdate,
    user=Depends(get_current_user)
):

    appointment = (
        supabase_admin
        .table("appointments")
        .select("patient_id")
        .eq("id", appointment_id)
        .single()
        .execute()
    )

    if not appointment.data:
        raise HTTPException(
            404,
            "Appointment not found"
        )

    require_patient_access_manual(
        patient_id=appointment.data["patient_id"],
        user_id=user["id"]
    )

    return update_appointment(
        appointment_id=appointment_id,
        payload=payload
    )