from decimal import Decimal, ROUND_HALF_UP

from domain.constants.GainStrategy import GainStrategy
from domain.entities.result.Result import Result
from domain.exceptions.DomainException import DomainException
from domain.valueObject.Money import Money


class PriceCalculator:

    @staticmethod
    def calculate(
        purchase_price: Money,
        gain_strategy: GainStrategy,
        gain_amount: Money
    ) -> Result[Money]:

        if purchase_price is None:
            return Result.failure(
                "Se necesita un precio de compra para calcular el precio."
            )

        if gain_strategy is None:
            return Result.failure(
                "Se necesita una estrategia de ganancia para calcular el precio."
            )

        if gain_amount is None:
            return Result.failure(
                "Se necesita un monto de ganancia para calcular el precio."
            )

        if gain_strategy == GainStrategy.INCREMENTAL:
            final_price = purchase_price.value + gain_amount.value

        elif gain_strategy == GainStrategy.PORCENTAJE:
            percentage = (
                gain_amount.value / Decimal("100")
            )

            final_price = purchase_price.value * (
                Decimal("1") + percentage
            )

            final_price = final_price.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

        else:
            return Result.failure(
                "Estrategia de ganancia no soportada."
            )

        try:
            return Result.success(
                Money(final_price)
            )

        except DomainException as e:
            return Result.failure(
                str(e)
            )