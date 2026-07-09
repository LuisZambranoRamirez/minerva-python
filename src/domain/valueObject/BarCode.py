from domain.exceptions.DomainException import DomainException
from domain.interfaces.ValueObject import ValueObject

class BarCode(ValueObject[str]):

    def __init__(self, value: str):
        super().__init__(value)

        if value.isspace() or value == "":
            raise DomainException("El código de barras no puede estar vacío.")

        if len(value) != 13:
            raise DomainException("El código de barras debe tener 13 dígitos.")

        if not value.isdigit():
            raise DomainException("El código de barras solo puede contener números.")