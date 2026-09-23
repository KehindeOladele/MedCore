import json
from typing import Any

from app.core.fhir.exceptions import FHIRSerializationError
from app.core.fhir.resource import FHIRResource


def serialize_resource(resource: FHIRResource) -> str:
    """
    Serialize a FHIR resource into JSON.

    Raises:
        FHIRSerializationError: If the resource cannot be serialized.
    """
    if not isinstance(resource, FHIRResource):
        raise FHIRSerializationError(
            "Object must be a FHIRResource."
        )

    try:
        return json.dumps(
            resource.to_dict(),
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as exc:
        raise FHIRSerializationError(
            "Failed to serialize FHIR resource."
        ) from exc


def resource_to_dict(resource: FHIRResource) -> dict[str, Any]:
    """
    Return the dictionary representation of a FHIR resource.

    Raises:
        FHIRSerializationError: If the resource is not a FHIRResource.
    """
    if not isinstance(resource, FHIRResource):
        raise FHIRSerializationError(
            "Object must be a FHIRResource."
        )

    try:
        return resource.to_dict()
    except (TypeError, ValueError) as exc:
        raise FHIRSerializationError(
            "Failed to convert FHIR resource to dictionary."
        ) from exc