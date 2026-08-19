"""
Healthcare Service domain exceptions.

These exceptions represent business/domain errors only.
They intentionally contain no FastAPI or HTTP concepts.
"""

from app.modules.organizations.exceptions import OrganizationError


# ---------------------------------------------------------------------
# Base Exception
# ---------------------------------------------------------------------

class HealthcareServiceError(OrganizationError):
    """
    Base exception for all Healthcare Service domain errors.
    """

    pass


# ---------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------

class HealthcareServiceNotFoundError(HealthcareServiceError):
    default_message = "Healthcare service not found."


class HealthcareServiceAlreadyExistsError(HealthcareServiceError):
    default_message = (
        "A healthcare service with this name already exists."
    )

# ---------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------

class HealthcareServiceInactiveError(HealthcareServiceError):
    default_message = (
        "The healthcare service is inactive."
    )


class HealthcareServiceAlreadyActiveError(
    HealthcareServiceError
):
    default_message = (
        "The healthcare service is already active."
    )