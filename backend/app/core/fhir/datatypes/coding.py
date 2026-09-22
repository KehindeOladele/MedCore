from dataclasses import dataclass


@dataclass(frozen=True)
class FHIRCoding:
    """
    Represents a FHIR Coding datatype.
    """

    system: str | None = None
    version: str | None = None
    code: str | None = None
    display: str | None = None
    user_selected: bool | None = None

    def to_dict(self) -> dict:
        data = {}

        if self.system is not None:
            data["system"] = self.system

        if self.version is not None:
            data["version"] = self.version

        if self.code is not None:
            data["code"] = self.code

        if self.display is not None:
            data["display"] = self.display

        if self.user_selected is not None:
            data["userSelected"] = self.user_selected

        return data