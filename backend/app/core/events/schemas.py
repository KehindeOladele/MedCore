# ----- Event Type Models -----
class EventTypes:
    PATIENT_CREATED = "patient.created"
    ONBOARDING_EMAIL_REQUESTED = (
        "onboarding.email_requested"
    )
    ONBOARDING_EMAIL_SENT = (
        "onboarding.email_sent"
    )
    ONBOARDING_EMAIL_FAILED = (
        "onboarding.email_failed"
    )
    ORGANIZATION_CREATED = "organization.created"

    ORGANIZATION_ONBOARDING_REQUESTED = (
        "organization.onboarding.requested"
    )

    ORGANIZATION_ONBOARDING_COMPLETED = (
        "organization.onboarding.completed"
    )


# ----- Event Status Model -----
class EventStatus:
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"
    DEAD = "dead"