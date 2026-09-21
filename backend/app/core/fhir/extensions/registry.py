from app.core.fhir.exceptions import FHIRResourceError
from app.core.fhir.extensions.definitions import (
    FHIRPrimitiveExtensionDefinition,
)


class FHIRExtensionRegistry:
    """
    Central registry for MedCore FHIR extension definitions.

    Extension definitions are registered by name and canonical URL.
    """

    def __init__(self) -> None:
        self._definitions: dict[
            str,
            FHIRPrimitiveExtensionDefinition,
        ] = {}

    def register(
        self,
        definition: FHIRPrimitiveExtensionDefinition,
    ) -> None:
        """
        Register a FHIR extension definition.

        Raises:
            FHIRResourceError:
                If the name or canonical URL is already registered.
        """
        if not isinstance(
            definition,
            FHIRPrimitiveExtensionDefinition,
        ):
            raise FHIRResourceError(
                "Extension definition must be a "
                "FHIRPrimitiveExtensionDefinition."
            )

        if definition.name in self._definitions:
            raise FHIRResourceError(
                f"FHIR extension name already registered: "
                f"{definition.name}"
            )

        if any(
            existing.url == definition.url
            for existing in self._definitions.values()
        ):
            raise FHIRResourceError(
                f"FHIR extension URL already registered: "
                f"{definition.url}"
            )

        self._definitions[definition.name] = definition

    def get(
        self,
        name: str,
    ) -> FHIRPrimitiveExtensionDefinition:
        """
        Retrieve an extension definition by name.

        Raises:
            FHIRResourceError:
                If the extension is not registered.
        """
        try:
            return self._definitions[name]
        except KeyError as exc:
            raise FHIRResourceError(
                f"FHIR extension is not registered: {name}"
            ) from exc

    def contains(self, name: str) -> bool:
        """
        Return whether an extension is registered.
        """
        return name in self._definitions

    def all(
        self,
    ) -> tuple[FHIRPrimitiveExtensionDefinition, ...]:
        """
        Return all registered extension definitions.
        """
        return tuple(self._definitions.values())