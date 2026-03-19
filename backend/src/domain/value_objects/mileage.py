from dataclasses import dataclass


@dataclass(frozen=True)
class Mileage:
    """Odometer reading in kilometres."""

    km: int

    def __post_init__(self) -> None:
        if self.km < 0:
            raise ValueError(f"Mileage can't be negative, got {self.km}")
