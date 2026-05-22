from typing import Final
import re

class PhoneNumber:
    LENGTH: Final[int] = 9

    def __init__(self, value: str):
        if value is None:
            raise ValueError("Ingrese un número de teléfono.")

        if len(value) != self.LENGTH:
            raise ValueError(
                f"El número de teléfono debe tener {self.LENGTH} dígitos."
            )

        if not re.fullmatch(r"\d+", value):
            raise ValueError(
                "El número de teléfono solo puede contener números."
            )
            
        self.value: Final[str] = value
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PhoneNumber):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
