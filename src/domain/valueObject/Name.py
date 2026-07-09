import re

from domain.exceptions.DomainException import DomainException
from domain.interfaces.ValueObject import ValueObject


class Name(ValueObject[str]):

    MIN_LENGTH = 3
    MAX_LENGTH = 50

    def __init__(
        self,
        value: str,
        min_length: int = MIN_LENGTH,
        max_length: int = MAX_LENGTH
    ):
        super().__init__(value)

        self._validate(value, min_length, max_length)

    def _validate(
        self,
        value: str,
        min_length: int,
        max_length: int
    ) -> None:
        if value.isspace() or value == "":
            raise DomainException("El NOMBRE no puede estar vacío.")

        if len(value) < min_length:
            raise DomainException(
                f"El NOMBRE debe tener al menos {min_length} caracteres."
            )

        if len(value) > max_length:
            raise DomainException(
                f"El NOMBRE no puede exceder los {max_length} caracteres."
            )

        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$", value):
            raise DomainException("El NOMBRE solo debe contener letras.")