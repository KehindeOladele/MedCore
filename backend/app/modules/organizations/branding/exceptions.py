from app.modules.organizations.exceptions import OrganizationError


# -----------------------------------------------------------------------------------
# BRANDING EXCEPTIONS
# -----------------------------------------------------------------------------------
class BrandingError(OrganizationError):
    """Base error for organization-branding operations."""


# -----------------------------------------------------------------------------------
# BRANDIING-SPECIFIC EXCEPTIONS
# -----------------------------------------------------------------------------------
class BrandingNotFoundError(BrandingError):
    default_message = "Organization branding was not found."


# -----------------------------------------------------------------------------------
# LOGO UPLOAD EXCEPTIONS
# -----------------------------------------------------------------------------------
class InvalidLogoError(BrandingError):
    default_message = "Logo must be a PNG, JPEG, or WebP image no larger than 2 MB."
