from decimal import Decimal

from domain.exceptions.DomainException import DomainException
from domain.exceptions.MinimumAmountException import MinimumAmountException
from domain.exceptions.UnexpectedDomainException import UnexpectedDomainException
from domain.interfaces.ValueObject import ValueObject


class ProductQuantity(ValueObject[Decimal]):

    MIN_AMOUNT = Decimal("0")
    MAX_DECIMALS = 3

    def __init__(self, value: Decimal):
        super().__init__(value)

        if not value.is_finite():
            raise DomainException("La cantidad debe ser un valor válido.")

        exponent = value.as_tuple().exponent

        if isinstance(exponent, int):
            decimals = max(0, -exponent)

            if decimals > self.MAX_DECIMALS:
                raise DomainException(
                    "La cantidad no puede tener decimales."
                )

        if value < self.MIN_AMOUNT:
            raise MinimumAmountException(str(self.MIN_AMOUNT))

    @staticmethod
    def zero() -> "ProductQuantity":
        try:
            return ProductQuantity(Decimal("0"))

        except DomainException as e:
            raise UnexpectedDomainException(
                "Error al crear la cantidad cero.",
                e,
            )

    def is_greater_than_zero(self) -> bool:
        return self.value > Decimal("0")

    def is_less_than_zero(self) -> bool:
        return self.value < Decimal("0")

    def is_zero(self) -> bool:
        return self.value == Decimal("0")

    def is_zero_or_less(self) -> bool:
        return self.value <= Decimal("0")

    # --------------------- COMPARACIONES ---------------------

    def is_greater_than(self, other: "ProductQuantity") -> bool:
        return self.value > other.value

    def is_less_than(self, other: "ProductQuantity") -> bool:
        return self.value < other.value

    def add(self, other: "ProductQuantity") -> "ProductQuantity":
        try:
            return ProductQuantity(self.value + other.value)

        except DomainException as e:
            raise UnexpectedDomainException(
                f"Error al sumar cantidades de producto: {str(e)}",
                e,
            )

    def subtract(self, other: "ProductQuantity") -> "ProductQuantity":
        try:
            return ProductQuantity(self.value - other.value)

        except MinimumAmountException:
            raise

        except DomainException as e:
            raise UnexpectedDomainException(
                f"Error al restar cantidades de producto: {str(e)}",
                e,
            )

    def is_decimal(self) -> bool:
        exponent = self.value.as_tuple().exponent

        if isinstance(exponent, int):
            return exponent < 0

        return False

    def is_integer(self) -> bool:
        return not self.is_decimal()