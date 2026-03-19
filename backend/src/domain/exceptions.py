class DomainError(Exception):
    """Base for all domain-level errors."""


class CarNotFound(DomainError):
    def __init__(self, car_id: str) -> None:
        super().__init__(f"Car '{car_id}' not found")
        self.car_id = car_id


class InvalidCredentials(DomainError):
    def __init__(self) -> None:
        super().__init__("Wrong username or password")


class ScraperError(DomainError):
    """Raised when the scraper fails to fetch or parse a page."""
