from app.core.fhir.exceptions import FHIRValidationError
from app.core.fhir.resource import FHIRResource


def validate_resource(resource: FHIRResource) -> None:
    """
    Validate the basic structure of a FHIR resource.

    Raises:
        FHIRValidationError: If the resource is structurally invalid.
    """
    if not isinstance(resource, FHIRResource):
        raise FHIRValidationError(
            "Object must be a FHIRResource."
        )

    if not resource.resource_type:
        raise FHIRValidationError(
            "FHIR resource must define a resourceType."
        )

    if not isinstance(resource.resource_type, str):
        raise FHIRValidationError(
            "FHIR resourceType must be a string."
        )

    if resource.id is not None and not isinstance(resource.id, str):
        raise FHIRValidationError(
            "FHIR resource id must be a string."
        )

    if resource.meta is not None and not isinstance(resource.meta, dict):
        raise FHIRValidationError(
            "FHIR resource meta must be a dictionary."
        )

    try:
        data = resource.to_dict()
    except Exception as exc:
        raise FHIRValidationError(
            "FHIR resource could not be serialized for validation."
        ) from exc

    if not isinstance(data, dict):
        raise FHIRValidationError(
            "FHIR resource serialization must return a dictionary."
        )

    if "resourceType" not in data:
        raise FHIRValidationError(
            "FHIR resource serialization must define resourceType."
        )

    if not isinstance(data["resourceType"], str):
        raise FHIRValidationError(
            "FHIR serialized resourceType must be a string."
        )

    if data["resourceType"] != resource.resource_type:
        raise FHIRValidationError(
            "FHIR serialized resourceType does not match the resource."
        )