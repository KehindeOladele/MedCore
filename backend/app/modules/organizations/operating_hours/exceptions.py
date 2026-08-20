"""Domain errors for organization operating hours."""

from app.modules.organizations.exceptions import OrganizationError


class OperatingHoursError(OrganizationError):
    """Base error for operating-hours operations."""


class OperatingHoursNotFoundError(OperatingHoursError):
    default_message = "Operating-hours entry not found."


class OperatingHoursConflictError(OperatingHoursError):
    default_message = "Operating-hours entries for this day overlap or conflict."
