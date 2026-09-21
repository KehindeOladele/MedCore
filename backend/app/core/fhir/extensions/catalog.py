from app.core.config import settings
from app.core.fhir.extensions.definitions import (
    FHIRPrimitiveExtensionDefinition,
)


ORGANIZATION_DESCRIPTION = "organization-description"
ORGANIZATION_TIMEZONE = "organization-timezone"

ORGANIZATION_PRIMARY_COLOR = "organization-primary-color"
ORGANIZATION_SECONDARY_COLOR = "organization-secondary-color"


def _extension_url(name: str) -> str:
    """
    Build the canonical URL for a FHIR extension.

    The canonical base URL must be configured before
    application-level extension definitions are created.
    """
    if not settings.FHIR_CANONICAL_BASE_URL:
        raise RuntimeError(
            "FHIR_CANONICAL_BASE_URL must be configured "
            "before creating FHIR extension definitions."
        )

    return (
        f"{settings.FHIR_CANONICAL_BASE_URL.rstrip('/')}"
        f"/{name}"
    )


def organization_description_extension() -> FHIRPrimitiveExtensionDefinition:
    return FHIRPrimitiveExtensionDefinition(
        name=ORGANIZATION_DESCRIPTION,
        url=_extension_url(ORGANIZATION_DESCRIPTION),
        value_type="string",
        context="Organization",
        description="Additional MedCore organization description.",
    )


def organization_timezone_extension() -> FHIRPrimitiveExtensionDefinition:
    return FHIRPrimitiveExtensionDefinition(
        name=ORGANIZATION_TIMEZONE,
        url=_extension_url(ORGANIZATION_TIMEZONE),
        value_type="string",
        context="Organization",
        description="MedCore organization timezone.",
    )


def organization_primary_color_extension() -> FHIRPrimitiveExtensionDefinition:
    return FHIRPrimitiveExtensionDefinition(
        name=ORGANIZATION_PRIMARY_COLOR,
        url=_extension_url(ORGANIZATION_PRIMARY_COLOR),
        value_type="string",
        context="Organization",
        description="MedCore organization primary branding color.",
    )


def organization_secondary_color_extension() -> FHIRPrimitiveExtensionDefinition:
    return FHIRPrimitiveExtensionDefinition(
        name=ORGANIZATION_SECONDARY_COLOR,
        url=_extension_url(ORGANIZATION_SECONDARY_COLOR),
        value_type="string",
        context="Organization",
        description="MedCore organization secondary branding color.",
    )