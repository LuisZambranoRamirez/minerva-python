from domain.entities.shared.Result import Result
from dataclasses import dataclass
from decimal import Decimal


MIN_AMOUNT = Decimal("0")
MAX_DECIMALS = 2


@dataclass(frozen=True)
class Money:
    value: Decimal

    @staticmethod
    def of(value: Decimal) -> Result["Money"]:
        if value is None:
            return Result.fail("Ingrese el monto.")

        numDecimals = abs(int(value.as_tuple().exponent))

        if numDecimals > MAX_DECIMALS:
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