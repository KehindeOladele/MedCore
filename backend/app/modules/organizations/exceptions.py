"""
Organization domain exceptions.

These exceptions represent business/domain errors only.
They are intentionally framework-agnostic and should not
depend on FastAPI or HTTP concepts.
"""


# ---------------------------------------------------------
# Base Organization Exception
# ---------------------------------------------------------
class OrganizationError(Exception):
    """
    Base exception for all organization domain errors.
    """

    default_message = "Organization error."

    def __init__(self, message: str | None = None):
        super().__init__(message or self.default_message)


# ---------------------------------------------------------
# Organization Exceptions
# ---------------------------------------------------------
class UserOrganizationNotFoundError(OrganizationError):
    """
    Raised when a user's organization cannot be found.
    """

    default_message = (
        "User organization could not be found."
    )


class OrganizationNotFoundError(OrganizationError):
    """
    Raised when an organization does not exist.
    """

    default_message = (
        "Organization not found."
    )


class OrganizationAccessDeniedError(OrganizationError):
    """
    Raised when a user attempts to access an organization
    they are not authorized to access.
    """

    default_message = (
        "You do not have permission to access this organization."
    )


class OrganizationMembershipRequiredError(
    OrganizationError
):
    """
    Raised when organization membership is required.
    """

    default_message = (
        "Organization membership is required."
    )


class OrganizationAdminRequiredError(
    OrganizationError
):
    """
    Raised when administrator privileges are required.
    """

    default_message = (
        "Organization administrator privileges are required."
    )


class OrganizationInactiveError(OrganizationError):
    """
    Raised when an operation requires an active organization.
    """

    default_message = (
        "The organization is inactive."
    )


# ---------------------------------------------------------
# Organization Onboarding Exceptions
# ---------------------------------------------------------
class OrganizationOnboardingError(
    OrganizationError
):
    """
    Base exception for onboarding workflow failures.
    """

    default_message = (
        "Organization onboarding failed."
    )


class EmailDeliveryError(
    OrganizationOnboardingError
):
    """
    Raised when onboarding email delivery fails.
    """

    default_message = (
        "Unable to deliver onboarding email."
    )


class InvalidOrganizationEmailError(
    OrganizationOnboardingError
):
    """
    Raised when the organization's email is invalid.
    """

    default_message = (
        "Organization email is missing or invalid."
    )


# ---------------------------------------------------------
# Organization Profile Exceptions
# ---------------------------------------------------------
class OrganizationProfileError(
    OrganizationError
):
    """
    Base exception for organization profile operations.
    """

    default_message = (
        "Organization profile operation failed."
    )


class OrganizationProfileValidationError(
    OrganizationProfileError
):
    """
    Raised when organization profile validation fails.
    """

    default_message = (
        "Organization profile validation failed."
    )


class OrganizationProfileUpdateError(
    OrganizationProfileError
):
    """
    Raised when updating an organization profile fails.
    """

    default_message = (
        "Failed to update organization profile."
    )


# ---------------------------------------------------------
# Organization Shared Department Exceptions
# ---------------------------------------------------------
class DepartmentNotFoundError(OrganizationError):
    """
    Raised when the referenced department does not exist.
    """

    default_message = (
        "Department not found."
    )


class DepartmentInactiveError(OrganizationError):
    """
    Raised when the referenced department is inactive.
    """

    default_message = (
        "The department is inactive."
    )