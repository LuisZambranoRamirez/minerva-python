from typing import Final
import re

from domain.exceptions.domainException import DomainException 

class RUC:
    LENGTH: Final[int] = 11

    def __init__(self, value: str):
        if value is None:
            raise DomainException("El RUC no puede ser nulo.")

        if len(value) != self.LENGTH:
            raise DomainException(
                f"El RUC debe tener exactamente {self.LENGTH} caracteres."
            )

        if not re.fullmatch(r"\d+", value):
            raise DomainException("El RUC debe contener solo números.")

        self._value: Final[str] = value

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RUC):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)
