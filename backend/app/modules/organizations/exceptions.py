"""
Organization module exceptions.
"""


class OrganizationError(Exception):
    """Base exception for organization-related errors."""
    pass


class OrganizationNotFoundError(OrganizationError):
    """Raised when an organization cannot be found."""
    pass


class OrganizationOnboardingError(OrganizationError):
    """Base exception for onboarding workflow failures."""
    pass


class EmailDeliveryError(OrganizationOnboardingError):
    """Raised when the welcome email cannot be delivered."""
    pass


class InvalidOrganizationEmailError(OrganizationOnboardingError):
    """Raised when the organization's email is missing or invalid."""
    pass