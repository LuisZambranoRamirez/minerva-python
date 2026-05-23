from domain.exceptions.domainException import DomainException 
from typing import Final
import re


class CustomerId:
    MIN_LENGTH: Final[int] = 3
    MAX_LENGTH: Final[int] = 100
    PATTERN: Final[re.Pattern] = re.compile(r"^[A-Za-zñÑ0-9 ]+$")

    def __init__(self, value: str):
        if value is None:
            raise DomainException("El NOMBRE DEL CLIENTE no puede ser nulo.")

        value = value.strip()

        if value == "":
            raise DomainException("El NOMBRE DEL CLIENTE no puede estar vacío.")

        if len(value) < self.MIN_LENGTH:
            raise DomainException(
                f"El NOMBRE DEL CLIENTE debe tener al menos {self.MIN_LENGTH} caracteres."
            )

        if len(value) > self.MAX_LENGTH:
            raise DomainException(
                f"El NOMBRE DEL CLIENTE no puede exceder los {self.MAX_LENGTH} caracteres."
            )

        if not self.PATTERN.fullmatch(value):
            raise DomainException(
                "El NOMBRE DEL CLIENTE solo debe contener letras (sin tildes) y números."
            )

        self.value: Final[str] = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CustomerId):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)