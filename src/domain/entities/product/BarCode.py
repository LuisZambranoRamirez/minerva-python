from typing import Final
import re

class BarCode:
    LENGTH: Final[int] = 13

    def __init__(self, value: str):
        if value is None:
            raise ValueError("Ingrese el código de barras.")

        if not value or not value.strip():
            raise ValueError("El código de barras no puede estar vacío.")

        if len(value) != self.LENGTH:
            raise ValueError(
                f"El código de barras debe tener {self.LENGTH} dígitos."
            )

        if not re.fullmatch(r"\d+", value):
            raise ValueError("El código de barras solo puede contener números.")

        self.value: Final[str] = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BarCode):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
