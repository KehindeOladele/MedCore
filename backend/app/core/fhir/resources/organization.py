from app.core.fhir.constants import FHIR_RESOURCE_ORGANIZATION
from app.core.fhir.resource import FHIRResource


class FHIROrganization(FHIRResource):
    """
    Base FHIR Organization resource representation.

    Resource-specific fields will be introduced incrementally
    in later Phase 3 steps.
    """

    resource_type = FHIR_RESOURCE_ORGANIZATION