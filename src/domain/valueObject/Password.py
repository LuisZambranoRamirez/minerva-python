from domain.exceptions.DomainException import DomainException
from domain.interfaces.ValueObject import ValueObject


class Password(ValueObject[str]):

    MIN_LENGTH = 8
    MAX_LENGTH = 100

    def __init__(self, value: str):
        super().__init__(value)

        if value.isspace() or value == "":
            raise DomainException("El PASSWORD no puede estar vacío.")

        if len(value) < self.MIN_LENGTH:
            raise DomainException(
                f"El PASSWORD debe tener al menos {self.MIN_LENGTH} caracteres."
            )

        if len(value) > self.MAX_LENGTH:
            raise DomainException(
                f"El PASSWORD no puede exceder los {self.MAX_LENGTH} caracteres."
            )