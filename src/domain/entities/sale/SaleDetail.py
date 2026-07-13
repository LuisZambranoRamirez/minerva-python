from decimal import ROUND_HALF_UP
from decimal import Decimal

from domain.entities.product.ProductId import ProductId
from domain.entities.sale.SaleDetailId import SaleDetailId
from domain.exceptions.DomainException import DomainException
from domain.exceptions.UnexpectedDomainException import UnexpectedDomainException
from domain.interfaces.Entity import Entity
from domain.valueObject.Money import Money
from domain.valueObject.ProductQuantity import ProductQuantity
from domain.valueObject.id.ProductName import ProductName
from domain.valueObject.id.SaleDetailIdImpl import SaleDetailIdImpl


class SaleDetail(Entity[SaleDetailId]):

    def __init__(
        self,
        product_name: ProductName,
        quantity: ProductQuantity,
        unit_price: Money
    ):
        if product_name is None:
            raise DomainException(
                "Debe ingresar el nombre del producto"
            )

        if (
            quantity is not None
            and quantity.is_zero_or_less()
        ):
            raise DomainException(
                "La CANTIDAD DE PRODUCTO debe ser mayor a 0."
            )

        if (
            unit_price is not None
            and unit_price.is_zero_or_less()
        ):
            raise DomainException(
                "El PRECIO UNITARIO debe ser mayor a 0."
            )

        super().__init__(
            SaleDetailIdImpl.generate()
        )

        self._product_name = product_name
        self._quantity = quantity
        self._unit_price = unit_price

    @classmethod
    def restore(
        cls,
        id: str,
        product_name: str,
        quantity: Decimal,
        unit_price: Decimal
    ) -> "SaleDetail":

        try:
            detail = cls.__new__(cls)

            temp_id = SaleDetailIdImpl.from_string(
                id
            )

            Entity.__init__(
                detail,
                temp_id
            )

            detail._product_name = ProductName(
                product_name
            )

            detail._quantity = ProductQuantity(
                quantity
            )

            detail._unit_price = Money(
                unit_price
            )

            return detail

        except DomainException as e:
            raise UnexpectedDomainException(
                f"Error al crear el detalle de venta: {str(e)}",
                e
            )

    def calculate_sub_total(self) -> Money:
        try:
            subtotal = (
                self._unit_price.value *
                self._quantity.value
            )
            print("Valor antes de redondear:", subtotal)
            print("Decimales:", subtotal.as_tuple().exponent)

            subtotal = subtotal.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

            print("Valor después de redondear:", subtotal)
            print("Decimales:", subtotal.as_tuple().exponent)

            return Money(subtotal)

        except DomainException as e:
            raise UnexpectedDomainException(
                f"Error al calcular el subtotal del detalle de venta: {str(e)}",
                e
            )

    def get_product_id(self) -> ProductId:
        return self._product_name

    def get_quantity(self) -> ProductQuantity:
        return self._quantity

    def get_unit_price(self) -> Money:
        return self._unit_price