import re

from domain.entities.user.UserId import UserId
from domain.exceptions.DomainException import DomainException
from domain.interfaces.ValueObject import ValueObject


class UserName(ValueObject[str], UserId):

    MIN_LENGTH = 3
    MAX_LENGTH = 30

    def __init__(self, value: str):
        super().__init__(value)

        if value == "" or value.isspace():
            raise DomainException(
                "El USERNAME no puede estar vacío."
            )

        if len(value) < self.MIN_LENGTH:
            raise DomainException(
                f"El USERNAME debe tener al menos {self.MIN_LENGTH} caracteres."
            )

        if len(value) > self.MAX_LENGTH:
            raise DomainException(
                f"El USERNAME no puede exceder los {self.MAX_LENGTH} caracteres."
            )

        if not re.match(r"^[a-zA-Z0-9]+$", value):
            raise DomainException(
                "El USERNAME solo puede contener letras (sin tilde) y números"
            )

    def get_value(self) -> str:
        return self.value

    def as_string(self) -> str:
        return self.value