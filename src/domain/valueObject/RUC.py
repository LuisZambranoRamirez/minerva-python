from domain.exceptions.DomainException import DomainException
from domain.interfaces.ValueObject import ValueObject


class RUC(ValueObject[str]):

    LENGTH = 11

    def __init__(self, value: str):
        super().__init__(value)

        if len(value) != self.LENGTH:
            raise DomainException(
                f"El RUC debe tener exactamente {self.LENGTH} caracteres."
            )

        if not value.isdigit():
            raise DomainException(
                "El RUC debe contener solo números."
            )