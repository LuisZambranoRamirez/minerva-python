from domain.exceptions.DomainException import DomainException
from domain.interfaces.ValueObject import ValueObject


class DNI(ValueObject[str]):

    LENGTH = 8

    def __init__(self, value: str):
        super().__init__(value)

        if value.isspace() or value == "":
            raise DomainException("El DNI no puede estar vacío.")

        if not value.isdigit():
            raise DomainException("El DNI solo puede contener números.")

        if len(value) != self.LENGTH:
            raise DomainException(
                f"El DNI debe tener exactamente {self.LENGTH} dígitos."
            )