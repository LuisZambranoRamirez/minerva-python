from domain.exceptions.DomainException import DomainException
from domain.interfaces.ValueObject import ValueObject


class PhoneNumber(ValueObject[str]):

    LENGTH = 9

    def __init__(self, value: str):
        super().__init__(value)

        if len(value) != self.LENGTH:
            raise DomainException(
                f"El número de teléfono debe tener {self.LENGTH} dígitos."
            )

        if not value.isdigit():
            raise DomainException(
                "El número de teléfono solo puede contener números."
            )