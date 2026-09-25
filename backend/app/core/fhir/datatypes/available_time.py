from dataclasses import dataclass, field


@dataclass(frozen=True)
class FHIRAvailableTime:
    """
    Represents a FHIR HealthcareService.availableTime component.
    """

    days_of_week: tuple[str, ...] = field(default_factory=tuple)
    all_day: bool | None = None
    available_start_time: str | None = None
    available_end_time: str | None = None

    def to_dict(self) -> dict:
        """
        Return the AvailableTime component in FHIR JSON-compatible form.
        """
        data: dict = {}

        if self.days_of_week:
            data["daysOfWeek"] = list(self.days_of_week)

        if self.all_day is not None:
            data["allDay"] = self.all_day

        if self.available_start_time is not None:
            data["availableStartTime"] = self.available_start_time

        if self.available_end_time is not None:
            data["availableEndTime"] = self.available_end_time

        return data