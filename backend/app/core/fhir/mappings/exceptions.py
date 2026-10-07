class FHIRMappingError(Exception):
    """
    Base exception for domain-to-FHIR mapping failures.
    """


class FHIRMappingInputError(FHIRMappingError):
    """
    Raised when mapper input cannot be mapped to the target FHIR resource.
    """


class FHIRMappingOutputError(FHIRMappingError):
    """
    Raised when a mapper cannot produce the expected FHIR representation.
    """