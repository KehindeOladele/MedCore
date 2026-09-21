from app.core.fhir.extensions.catalog import (
    organization_description_extension,
    organization_primary_color_extension,
    organization_secondary_color_extension,
    organization_timezone_extension,
)
from app.core.fhir.extensions.registry import (
    FHIRExtensionRegistry,
)


def build_fhir_extension_registry() -> FHIRExtensionRegistry:
    """
    Build the canonical registry containing all currently
    supported MedCore FHIR extensions.
    """
    registry = FHIRExtensionRegistry()

    registry.register(
        organization_description_extension()
    )
    registry.register(
        organization_timezone_extension()
    )
    registry.register(
        organization_primary_color_extension()
    )
    registry.register(
        organization_secondary_color_extension()
    )

    return registry