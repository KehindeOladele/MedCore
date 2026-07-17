"""
Organization module exceptions.
"""


class OrganizationError(Exception):
    """Base exception for organization-related errors."""
    pass


class UserOrganizationNotFoundError(OrganizationError):
    """Raised when an user organization cannot be found"""
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


class OrganizationProfileError(OrganizationError):
    """Base exception for organization profile operations."""
    pass


class OrganizationProfileValidationError(OrganizationProfileError):
    """Raised when organization profile validation fails."""
    pass


class OrganizationProfileUpdateError(OrganizationProfileError):
    """Raised when updating the organization profile fails."""
    pass