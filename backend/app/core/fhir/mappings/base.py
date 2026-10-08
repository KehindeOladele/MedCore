from typing import Protocol, TypeVar


DomainT = TypeVar("DomainT")
FHIRResourceT = TypeVar("FHIRResourceT")


class FHIRMapper(Protocol[DomainT, FHIRResourceT]):
    """
    Contract for pure MedCore domain-to-FHIR mappers.

    Implementations translate an existing MedCore domain object
    into its corresponding FHIR resource representation.

    Mappers must remain independent of:
    - database access
    - domain services
    - FastAPI
    - authorization
    - domain business rules
    """

    def to_fhir(self, value: DomainT) -> FHIRResourceT:
        """
        Convert a MedCore domain object into a FHIR resource.
        """
        ...