class FHIRException(Exception):
    """Base exception for all FHIR infrastructure errors."""


class FHIRValidationError(FHIRException):
    """Raised when a FHIR resource fails structural or semantic validation."""


class FHIRSerializationError(FHIRException):
    """Raised when a FHIR resource cannot be serialized correctly."""


class FHIRResourceError(FHIRException):
    """Raised when a FHIR resource cannot be created, resolved, or processed."""


class FHIRIdentifierError(FHIRException):
    """Raised when a FHIR resource identifier is invalid or cannot be resolved."""


class FHIRVersionError(FHIRException):
    """Raised when an unsupported or invalid FHIR version is requested."""