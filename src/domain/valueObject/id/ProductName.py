import re

from domain.entities.product.ProductId import ProductId
from domain.exceptions.DomainException import DomainException
from domain.interfaces.ValueObject import ValueObject


class ProductName(ValueObject[str], ProductId):

    MIN_LENGTH = 3
    MAX_LENGTH = 100

    def __init__(self, value: str):
        super().__init__(value)

        if value == "" or value.isspace():
            raise DomainException(
                "El nombre del producto no puede estar vacío."
            )

        if len(value) < self.MIN_LENGTH:
            raise DomainException(
                f"El nombre del producto debe tener al menos {self.MIN_LENGTH} caracteres."
            )

        if len(value) > self.MAX_LENGTH:
            raise DomainException(
                f"El nombre del producto no puede tener más de {self.MAX_LENGTH} caracteres."
            )

        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$", value):
            raise DomainException(
                "El nombre del producto solo puede contener letras y números."
            )

    def as_string(self) -> str:
        return self.value

    def get_value(self) -> str:
        return self.value