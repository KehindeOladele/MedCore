from app.core.fhir.constants import FHIR_RESOURCE_HEALTHCARE_SERVICE
from app.core.fhir.resource import FHIRResource


class FHIRHealthcareService(FHIRResource):
    """
    Base FHIR HealthcareService resource representation.

    Resource-specific fields will be introduced incrementally
    in later Phase 3 steps.
    """

    resource_type = FHIR_RESOURCE_HEALTHCARE_SERVICE