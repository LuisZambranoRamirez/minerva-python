from app.domain.entities.shared.Result import Result
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


MIN_AMOUNT = Decimal("0")
MAX_DECIMALS = 2


@dataclass(frozen=True)
class Money:
    value: Decimal

    @staticmethod
    def of(value: Optional[Decimal]):
        if value is None:
            return Result.fail("Ingrese el monto.")

        if value.as_tuple().exponent < -MAX_DECIMALS:
            return Result.fail(
                f"El monto solo puede tener {MAX_DECIMALS} decimales."
            )

        if value < MIN_AMOUNT:
            return Result.fail(
                f"El monto no puede ser menor que {MIN_AMOUNT}."
            )

        return Result.success(Money(value))

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