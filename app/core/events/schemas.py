# ----- Event Type Models -----
class EventTypes:

    # Patients EventTypes
    # -------------------
    PATIENT_CREATED = (
        "patient.created"
        )

    # Onboarding EventTypes
    # ---------------------
    ONBOARDING_EMAIL_REQUESTED = (
        "onboarding.email_requested"
    )

    ONBOARDING_EMAIL_SENT = (
        "onboarding.email_sent"
    )

    ONBOARDING_EMAIL_FAILED = (
        "onboarding.email_failed"
    )
    ORGANIZATION_CREATED = (
        "organization.created"
    )

    # Organization EventTypes
    # -----------------------
    ORGANIZATION_ONBOARDING_REQUESTED = (
        "organization.onboarding.requested"
    )

    ORGANIZATION_ONBOARDING_COMPLETED = (
        "organization.onboarding.completed"
    )

    ORGANIZATION_ONBOARDING_FAILED = (
        "organization.onboarding.failed"
    )

    ORGANIZATION_PROFILE_UPDATED = (
        "organization.profile.updated"
    )

    # Department EventTypes
    # ---------------------
    DEPARTMENT_CREATED = (
        "department.created"
    )

    DEPARTMENT_UPDATED = (
        "department.updated"
    )

    DEPARTMENT_DELETED = (
        "department.deleted"
    )

    DEPARTMENT_ONBOARDING_REQUESTED = (
        "department.onboarding.requested"
    )

    DEPARTMENT_ONBOARDING_COMPLETED = (
        "department.onboarding.completed"
    )


    # Healthcare_service EventTypes
    # -----------------------------
    HEALTHCARE_SERVICE_CREATED = (
        "healtcare_service.created"
    )

    HEALTHCARE_SERVICE_UPDATED = (
        "healtcare_service.updated"
    )

    HEALTHCARE_SERVICE_DELETED = (
    "healthcare_service.updated"
    )

    HEALTHCARE_SERVICE_ACTIVATED = (
    "healthcare_service.activated"
    )

    HEALTHCARE_SERVICE_DEACTIVATED = (
        "healthcare_service.deactivated"
    )

    # Organization Operating Hours EventTypes
    OPERATING_HOURS_CREATED = "operating_hours.created"
    OPERATING_HOURS_UPDATED = "operating_hours.updated"
    OPERATING_HOURS_DELETED = "operating_hours.deleted"

# ----- Event Status Model -----
class EventStatus:
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"
    DEAD = "dead"
