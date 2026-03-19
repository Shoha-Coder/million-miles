from dataclasses import dataclass


@dataclass(frozen=True)
class Price:
    """Yen amount. Immutable so it can be compared and hashed safely."""

    amount: int

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError(f"Price can't be negative, got {self.amount}")

    def in_man(self) -> float:
        """Convert to 万円 (10,000 yen units) — the standard Japanese display format."""
        return self.amount / 10_000
