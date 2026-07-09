import re

from domain.exceptions.DomainException import DomainException
from domain.interfaces.ValueObject import ValueObject


class LastName(ValueObject[str]):

    MIN_LENGTH = 3
    MAX_LENGTH = 50

    def __init__(self, value: str):
        super().__init__(value)

        if value.isspace() or value == "":
            raise DomainException("El APELLIDO no puede estar vacío.")

        if len(value) < self.MIN_LENGTH:
            raise DomainException(
                f"El APELLIDO debe tener al menos {self.MIN_LENGTH} caracteres."
            )

        if len(value) > self.MAX_LENGTH:
            raise DomainException(
                f"El APELLIDO no puede exceder los {self.MAX_LENGTH} caracteres."
            )

        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$", value):
            raise DomainException("El APELLIDO solo debe contener letras.")