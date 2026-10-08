from dataclasses import dataclass

from app.core.fhir.mappings.base import FHIRMapper


@dataclass
class DummyDomain:
    name: str


@dataclass
class DummyFHIR:
    name: str


class DummyMapper:
    def to_fhir(self, value: DummyDomain) -> DummyFHIR:
        return DummyFHIR(name=value.name)


def test_mapper_implements_to_fhir_contract():
    mapper: FHIRMapper[DummyDomain, DummyFHIR] = DummyMapper()

    result = mapper.to_fhir(DummyDomain(name="Example"))

    assert result == DummyFHIR(name="Example")