from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)  # Immutable Value Object
class Address:
    street: str
    city: str
    postal_code: str
    country: str
    apartment: Optional[str] = None
    
    def __post_init__(self):
        if not all([self.street, self.city, self.postal_code, self.country]):
            raise ValueError("All address fields are required")