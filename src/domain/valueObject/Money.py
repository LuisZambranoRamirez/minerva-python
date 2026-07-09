from decimal import Decimal

from domain.exceptions.DomainException import DomainException
from domain.exceptions.MinimumAmountException import MinimumAmountException
from domain.exceptions.UnexpectedDomainException import UnexpectedDomainException
from domain.interfaces.ValueObject import ValueObject


class Money(ValueObject[Decimal]):

    MIN_AMOUNT = Decimal("0")
    MAX_DECIMALS = 2

    def __init__(self, value: Decimal):
        super().__init__(value)

        if not value.is_finite():
            raise DomainException("El monto debe ser un valor válido.")

        exponent = value.as_tuple().exponent

        if isinstance(exponent, int):
            decimals = max(0, -exponent)

            if decimals > self.MAX_DECIMALS:
                raise DomainException(
                    f"El monto solo puede tener {self.MAX_DECIMALS} decimales."
                )

        if value < self.MIN_AMOUNT:
            raise MinimumAmountException(str(self.MIN_AMOUNT))

    def is_greater_than_zero(self) -> bool:
        return self.value > Decimal("0")

    def is_less_than_zero(self) -> bool:
        return self.value < Decimal("0")

    def is_zero(self) -> bool:
        return self.value == Decimal("0")

    def is_zero_or_less(self) -> bool:
        return self.value <= Decimal("0")

    def is_zero_or_greater(self) -> bool:
        return self.value >= Decimal("0")

    def is_less_than(self, other: "Money") -> bool:
        return self.value < other.value

    def is_greater_than(self, other: "Money") -> bool:
        return self.value > other.value

    def add(self, other: "Money") -> "Money":
        try:
            return Money(self.value + other.value)

        except DomainException as e:
            raise UnexpectedDomainException(
                f"Error al sumar montos: {str(e)}",
                e,
            )

    def subtract(self, other: "Money") -> "Money":
        try:
            return Money(self.value - other.value)

        except MinimumAmountException:
            raise

        except DomainException as e:
            raise UnexpectedDomainException(
                f"Error al restar montos: {str(e)}",
                e,
            )

    @staticmethod
    def zero() -> "Money":
        try:
            return Money(Decimal("0"))

        except DomainException as e:
            raise UnexpectedDomainException(
                "Error al crear el monto cero.",
                e,
            )

    @staticmethod
    def ten_cents() -> "Money":
        try:
            return Money(Decimal("0.10"))

        except DomainException as e:
            raise UnexpectedDomainException(
                "Error al crear el monto mínimo.",
                e,
            )