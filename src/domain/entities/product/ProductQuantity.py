from decimal import Decimal
from typing import Final, Self


class ProductQuantity:
    MIN_AMOUNT: Final[Decimal] = Decimal("0")
    MAX_DECIMALS: Final[int] = 3

    def __init__(self, value: Decimal):
        if value is None:
            raise ValueError("Ingrese la cantidad del producto.")

        # Calculamos la cantidad de decimales usando la tupla interna de Decimal
        num_decimals = abs(int(value.as_tuple().exponent))

        if num_decimals > self.MAX_DECIMALS:
            raise ValueError(
                f"El monto solo puede tener {self.MAX_DECIMALS} decimales."
            )

        if value < self.MIN_AMOUNT:
            raise ValueError(
                f"La cantidad no puede ser menor que {self.MIN_AMOUNT}."
            )

        self.value: Final[Decimal] = value

    @classmethod
    def zero(cls) -> Self:
        return cls(Decimal("0"))

    # --------------------- VALIDACIONES DE ESTADO ---------------------

    def is_greater_than_zero(self) -> bool:
        return self.value > 0

    def is_less_than_zero(self) -> bool:
        return self.value < 0

    def is_zero(self) -> bool:
        return self.value == 0

    def is_zero_or_less(self) -> bool:
        return self.value <= 0

    # --------------------- COMPARACIONES NATIVAS ---------------------

    def __gt__(self, other: "ProductQuantity") -> bool:
        """Sobrecarga del operador '>' (is_greater_than)."""
        if not isinstance(other, ProductQuantity):
            return NotImplemented
        return self.value > other.value

    def __lt__(self, other: "ProductQuantity") -> bool:
        """Sobrecarga del operador '<' (is_less_than)."""
        if not isinstance(other, ProductQuantity):
            return NotImplemented
        return self.value < other.value

    # --------------------- EQUALS & HASH ---------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ProductQuantity):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
