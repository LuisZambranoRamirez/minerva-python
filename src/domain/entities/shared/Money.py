from decimal import Decimal
from typing import Final

from domain.exceptions.domainException import DomainException 

class Money:
    MIN_AMOUNT: Final[Decimal] = Decimal("0")
    MAX_DECIMALS: Final[int] = 2

    def __init__(self, value: Decimal):
        if value is None:
            raise DomainException("Ingrese el monto.")

        num_decimals = abs(int(value.as_tuple().exponent))

        if num_decimals > self.MAX_DECIMALS:
            raise DomainException(
                f"El monto solo puede tener {self.MAX_DECIMALS} decimales."
            )

        if value < self.MIN_AMOUNT:
            raise DomainException(
                f"El monto no puede ser menor que {self.MIN_AMOUNT}."
            )

        self.value: Final[Decimal] = value

    def is_greater_than_zero(self) -> bool:
        return self.value > 0

    def is_less_than_zero(self) -> bool:
        return self.value < 0

    def is_zero(self) -> bool:
        return self.value == 0

    def is_zero_or_less(self) -> bool:
        return self.value <= 0

    def is_zero_or_greater(self) -> bool:
        return self.value >= 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)