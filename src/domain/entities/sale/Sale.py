from domain.entities.sale.DTO import SaleDetailDTO
from domain.entities.sale.DTO import PayDTO
from domain.entities.sale.DTO import PayData
from domain.entities.sale.DTO import SaleItem
from datetime import datetime
from decimal import Decimal
from typing import Dict, List

from domain.constants.PaymentMethod import PaymentMethod
from domain.entities.product.ProductId import ProductId
from domain.entities.result.Result import Result
from domain.entities.sale.Pay import Pay
from domain.entities.sale.SaleDetail import SaleDetail
from domain.entities.sale.SaleId import SaleId
from domain.exceptions.DomainException import DomainException
from domain.exceptions.UnexpectedDomainException import UnexpectedDomainException
from domain.interfaces.Entity import Entity
from domain.valueObject.Money import Money
from domain.valueObject.ProductQuantity import ProductQuantity
from domain.valueObject.id.CustomerName import CustomerName
from domain.valueObject.id.ProductName import ProductName
from domain.valueObject.id.SaleIdImpl import SaleIdImpl


class Sale(Entity[SaleId]):

    def __init__(
        self,
        customer_name_id: str,
        items: list[SaleItem]
    ):
        super().__init__(
            SaleIdImpl.generate()
        )

        self._customer_name = CustomerName(customer_name_id)
        self._pays: List[Pay] = []
        self._sale_details: Dict[ProductId, SaleDetail] = {}

        if items is None or len(items) == 0:
            raise DomainException(
                "La venta debe tener al menos un item"
            )

        for item in items:
            result = self.add_detail(
                item.product_id,
                item.unit_price,
                item.quantity
            )

            if result.is_failure():
                raise DomainException(
                    result.get_message()
                )

        self._registration_date = datetime.now()

    @classmethod
    def restore(
        cls,
        sale_id: str,
        customer_name_id: str,
        registration_date: datetime,
        sale_details: list,
        pays: list
    ) -> "Sale":

        try:
            sale = cls.__new__(cls)

            temp_id = SaleIdImpl.from_string(
                sale_id
            )

            Entity.__init__(
                sale,
                temp_id
            )

            sale._customer_name = CustomerName(
                customer_name_id
            )

            sale._registration_date = registration_date
            sale._sale_details = {}
            sale._pays = []

            if sale_details is None or len(sale_details) == 0:
                raise DomainException(
                    "La venta debe tener al menos un detalle"
                )

            for detail in sale_details:
                sale_detail = SaleDetail.restore(
                    id=detail.saledetailid,
                    product_name=detail.productnameid,
                    quantity=detail.quantity,
                    unit_price=detail.unitprice
                )

                sale._sale_details[
                    sale_detail.get_product_id()
                ] = sale_detail


            for pay in pays:
                sale._pays.append(
                    Pay.restore(
                        pay.payid,
                        pay.amount,
                        pay.paymentmethod,
                        pay.registrationdate
                    )
                )

            return sale

        except DomainException as e:
            raise UnexpectedDomainException(
                f"Error al crear la venta: {str(e)}",
                e
            )



    def add_detail(
        self,
        product_name_str: str,
        unit_price: Decimal,
        quantity_decimal: Decimal
    ) -> Result[None]:

        try:
            product_name = ProductName(
                product_name_str
            )

            price = Money(unit_price)
            quantity = ProductQuantity(
                quantity_decimal
            )

            if product_name in self._sale_details:
                existing = self._sale_details[product_name]

                quantity = quantity.add(
                    existing.get_quantity()
                )

                del self._sale_details[product_name]

            detail = SaleDetail(
                product_name,
                quantity,
                price
            )

            self._sale_details[
                product_name
            ] = detail

            return Result.success(None)

        except DomainException as e:
            return Result.failure(
                str(e)
            )

    def _add_payment(
        self,
        amount: Decimal,
        payment_method: PaymentMethod
    ) -> Result[None]:

        if self.is_due_canceled():
            return Result.failure(
                "La deuda de la venta ya esta saldada"
            )

        try:
            pay = Pay(
                Money(amount),
                payment_method
            )

        except DomainException as e:
            return Result.failure(
                str(e)
            )

        if pay.amount.is_greater_than(
            self.calculate_amount_due()
        ):
            return Result.failure(
                "El PAGO sobrepasa la DEUDA de la VENTA."
            )

        self._pays.append(pay)

        return Result.success(None)

    # ------------------------------------------

    def calculate_total(self) -> Money:
        total = Money.zero()

        for detail in self._sale_details.values():
            total = total.add(
                detail.calculate_sub_total()
            )

        return total

    def calculate_total_paid(self) -> Money:
        total = Money.zero()

        for pay in self._pays:
            total = total.add(
                pay.amount
            )

        return total

    def calculate_amount_due(self) -> Money:
        try:
            return self.calculate_total().subtract(
                self.calculate_total_paid()
            )

        except DomainException as e:
            raise UnexpectedDomainException(
                f"Error al calcular el monto adeudado: {str(e)}",
                e
            )

    def is_due_canceled(self) -> bool:
        return self.calculate_amount_due().is_zero()

    # ------------------------------------------

    @property
    def registration_date(self) -> datetime:
        return self._registration_date

    @property
    def customer_id(self) -> CustomerName:
        return self._customer_name

    def get_pays(self) -> list[PayDTO]:
        return [
            PayDTO(
                pay.id.as_string(),
                pay.amount.value,
                pay.payment_method,
                pay.registration_date
            )
            for pay in self._pays
        ]

    def get_sale_details(self) -> list[SaleDetailDTO]:
        return [
            SaleDetailDTO(
                detail.id.as_string(),
                detail.get_product_id().as_string(),
                detail.get_quantity().value,
                detail.get_unit_price().value
            )
            for detail in self._sale_details.values()
        ]

    def get_product_quantities(
        self
    ) -> dict[ProductId, ProductQuantity]:

        return {
            detail.get_product_id(): detail.get_quantity()
            for detail in self._sale_details.values()
        }