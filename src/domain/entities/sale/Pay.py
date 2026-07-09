from datetime import datetime
from decimal import Decimal

from domain.constants.PaymentMethod import PaymentMethod
from domain.entities.sale.PayId import PayId
from domain.exceptions.DomainException import DomainException
from domain.exceptions.UnexpectedDomainException import UnexpectedDomainException
from domain.interfaces.Entity import Entity
from domain.valueObject.Money import Money
from domain.valueObject.id.PayIdImpl import PayIdImpl


class Pay(Entity[PayId]):

    MIN_AMOUNT = Money.ten_cents()

    def __init__(
        self,
        amount: Money,
        payment_method: PaymentMethod
    ):
        if payment_method is None:
            raise DomainException(
                "El método de pago no puede estar vacío."
            )

        if (
            amount is not None
            and amount.is_less_than(self.MIN_AMOUNT)
        ):
            raise DomainException(
                f"El MONTO debe ser mayor o igual a S/{self.MIN_AMOUNT}"
            )

        super().__init__(
            PayIdImpl.generate()
        )

        self._amount = amount
        self._payment_method = payment_method
        self._registration_date = datetime.now()

    @classmethod
    def restore(
        cls,
        pay_id: str,
        amount: Decimal,
        payment_method: PaymentMethod,
        registration_date: datetime
    ) -> "Pay":

        try:
            pay = cls.__new__(cls)

            temp_id = PayIdImpl.from_string(pay_id)

            Entity.__init__(
                pay,
                temp_id
            )

            pay._amount = Money(amount)
            pay._payment_method = payment_method
            pay._registration_date = registration_date

            return pay

        except DomainException as e:
            raise UnexpectedDomainException(
                f"Error al crear el pago: {str(e)}",
                e,
            )

    @property
    def amount(self) -> Money:
        return self._amount

    @property
    def payment_method(self) -> PaymentMethod:
        return self._payment_method

    @property
    def registration_date(self) -> datetime:
        return self._registration_date