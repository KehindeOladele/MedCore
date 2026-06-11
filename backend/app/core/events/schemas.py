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


# ----- Event Status Model -----
class EventStatus:
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"
    DEAD = "dead"