from typing import Final
import re

from domain.exceptions.domainException import DomainException 

class SupplierId:
    MIN_LENGTH: Final[int] = 3
    MAX_LENGTH: Final[int] = 100

    def __init__(self, value: str):
        if value is None:
            raise DomainException("El NOMBRE DEL PROVEEDOR no puede ser nulo.")

        # .strip() elimina espacios en blanco al inicio y al final para validar si está vacío
        if not value or not value.strip():
            raise DomainException("El NOMBRE DEL PROVEEDOR no puede estar vacío.")

        if len(value) < self.MIN_LENGTH:
            raise DomainException(
                f"El NOMBRE DEL PROVEEDOR debe tener al menos {self.MIN_LENGTH} caracteres."
            )

        if len(value) > self.MAX_LENGTH:
            raise DomainException(
                f"El NOMBRE DEL PROVEEDOR no puede exceder los {self.MAX_LENGTH} caracteres."
            )

        if not re.fullmatch(r"[A-Za-zñÑ0-9 ]+", value):
            raise DomainException(
                "El NOMBRE DEL PROVEEDOR solo debe contener letras (sin tildes) y números."
            )

        self.value: Final[str] = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SupplierId):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)