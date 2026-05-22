from typing import Final
import re

class ProductId:
    MIN_LENGTH: Final[int] = 3
    MAX_LENGTH: Final[int] = 100

    def __init__(self, value: str):
        if value is None:
            raise ValueError("Ingrese el nombre del producto.")

        if not value or not value.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")

        if len(value) < self.MIN_LENGTH:
            raise ValueError(
                f"El nombre del producto debe tener al menos {self.MIN_LENGTH} caracteres."
            )

        if len(value) > self.MAX_LENGTH:
            raise ValueError(
                f"El nombre del producto no puede tener más de {self.MAX_LENGTH} caracteres."
            )

        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+", value):
            raise ValueError(
                "El nombre del producto solo puede contener letras y números."
            )

        self.value: Final[str] = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ProductId):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
