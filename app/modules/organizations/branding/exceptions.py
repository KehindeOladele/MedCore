from app.modules.organizations.exceptions import OrganizationError


class BrandingError(OrganizationError):
    """Base error for organization-branding operations."""


class BrandingNotFoundError(BrandingError):
    default_message = "Organization branding was not found."


class InvalidLogoError(BrandingError):
    default_message = "Logo must be a PNG, JPEG, or WebP image no larger than 2 MB."
