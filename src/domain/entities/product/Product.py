from domain.services.Math import Math
from datetime import datetime
from decimal import Decimal
from typing import Optional

from domain.constants.Category import Category
from domain.constants.GainStrategy import GainStrategy
from domain.constants.SaleType import SaleType
from domain.entities.product.ProductId import ProductId
from domain.entities.result.Result import Result
from domain.exceptions.DomainException import DomainException
from domain.exceptions.MinimumAmountException import MinimumAmountException
from domain.exceptions.UnexpectedDomainException import UnexpectedDomainException
from domain.interfaces.Entity import Entity
from domain.services.PriceCalculator import PriceCalculator
from domain.valueObject.BarCode import BarCode
from domain.valueObject.Money import Money
from domain.valueObject.ProductQuantity import ProductQuantity
from domain.valueObject.id.ProductName import ProductName


class Product(Entity[ProductId]):

    def __init__(
        self,
        product_name: str,
        gain_strategy: GainStrategy,
        gain_amount: Decimal,
        reorder_level: Optional[Decimal],
        bar_code: Optional[str],
        sale_type: SaleType,
        initial_stock: Decimal,
        category: Category,
        purchase_price: Decimal
    ):
        temp_id = ProductName(product_name)

        super().__init__(temp_id)

        self._product_name = temp_id
        self._stock = ProductQuantity(initial_stock)
        self._gain_amount = Money(gain_amount)
        self._gain_strategy = gain_strategy
        self._sale_type = sale_type
        self._category = category

        if gain_strategy is None:
            raise DomainException(
                "Seleccione una estrategia de ganancia."
            )

        if sale_type is None:
            raise DomainException(
                "Seleccione el tipo de venta."
            )

        if category is None:
            raise DomainException(
                "Seleccione una categoría."
            )

        if self._gain_amount.is_zero_or_less():
            raise DomainException(
                "El monto de ganancia debe ser mayor a cero."
            )

        if reorder_level is None:
            self._reorder_level = None
        else:
            quantity = ProductQuantity(reorder_level)

            if (
                sale_type == SaleType.UNIDAD
                and Math.is_decimal(quantity.value)
            ):
                raise DomainException(
                    "El nivel de reposición no puede ser decimal para productos vendidos por unidad."
                )

            self._reorder_level = quantity

        if bar_code is None:
            if sale_type == SaleType.UNIDAD:
                raise DomainException(
                    "Ingrese el código de barras para productos vendidos por unidad."
                )

            self._bar_code = None

        else:
            self._bar_code = BarCode(bar_code)

        price_result = PriceCalculator.calculate(
            Money(purchase_price),
            gain_strategy,
            self._gain_amount
        )

        if price_result.is_failure():
            raise DomainException(
                price_result.get_message()
            )

        price = price_result.get_data()

        if price is None:
            raise DomainException(
                "No se pudo calcular el precio del producto."
            )

        self._price = price
        self._registration_date = datetime.now()

    @classmethod
    def restore(
        cls,
        product_name: str,
        gain_strategy: GainStrategy,
        gain_amount: Decimal,
        reorder_level: Optional[Decimal],
        bar_code: Optional[str],
        sale_type: SaleType,
        stock: Decimal,
        category: Category,
        price: Decimal,
        registration_date: datetime
    ) -> "Product":

        try:
            product = cls.__new__(cls)

            temp_id = ProductName(product_name)

            Entity.__init__(product, temp_id)

            product._product_name = temp_id
            product._stock = ProductQuantity(stock)
            product._gain_amount = Money(gain_amount)
            product._gain_strategy = gain_strategy
            product._sale_type = sale_type
            product._category = category
            product._reorder_level = (
                ProductQuantity(reorder_level)
                if reorder_level is not None
                else None
            )
            product._bar_code = (
                BarCode(bar_code)
                if bar_code is not None
                else None
            )
            product._price = Money(price)
            product._registration_date = registration_date

            return product

        except DomainException as e:
            raise UnexpectedDomainException(
                f"Error al crear el producto: {str(e)}",
                e,
            )

    # -------------------------------

    def process_delivery_from_supplier(
        self,
        quantity: Decimal
    ) -> Result[None]:
        return self._increase_stock(quantity)

    def process_sale(
        self,
        quantity: Decimal
    ) -> Result[None]:
        return self._decrease_stock(quantity)

    def _increase_stock(
        self,
        quantity_to_add: Decimal
    ) -> Result[None]:

        try:
            new_stock = self._stock.add(
                ProductQuantity(quantity_to_add)
            )

            return self._update_stock(new_stock)

        except DomainException as e:
            return Result.failure(str(e))

    def _decrease_stock(
        self,
        quantity_to_subtract: Decimal
    ) -> Result[None]:

        if self._stock.is_zero():
            return Result.failure(
                "No hay stock disponible para este producto."
            )

        try:
            new_stock = self._stock.subtract(
                ProductQuantity(quantity_to_subtract)
            )

            self._update_stock(new_stock)

            return Result.success(None)

        except MinimumAmountException as e:

            if Math.is_zero_or_less(
                self._stock.value - quantity_to_subtract
            ):
                return Result.failure(
                    f"No hay suficiente stock para completar esta operación. Stock disponible: {self._stock.value}"
                )

            return Result.failure(str(e))

        except DomainException as e:
            return Result.failure(str(e))

    def _update_stock(
        self,
        new_stock_value: ProductQuantity
    ) -> Result[None]:

        if new_stock_value is None:
            return Result.failure(
                "El nuevo valor de stock no puede ser nulo."
            )

        if (
            self._sale_type == SaleType.UNIDAD
            and new_stock_value.is_decimal()
        ):
            return Result.failure(
                "Este producto se maneja por unidades. Ingrese una cantidad entera."
            )

        self._stock = new_stock_value

        return Result.success(None)

    # ---------------------------------------------

    def validate_bulk_association(
        self,
        bulk_product: "Product",
        quantity: ProductQuantity
    ) -> Result[None]:

        if bulk_product is None:
            return Result.failure(
                "El producto a granel no puede ser nulo."
            )

        if quantity is None:
            return Result.failure(
                "La cantidad no puede estar vacío"
            )

        if self == bulk_product:
            return Result.failure(
                "No es posible asociar un producto consigo mismo."
            )

        if self.get_sale_type() != SaleType.UNIDAD:
            return Result.failure(
                f"El producto -- {self.get_name_id()} -- se vende por unidad y no permite asociar otro producto."
            )

        if bulk_product.get_sale_type() != SaleType.GRANEL:
            return Result.failure(
                f"El producto -- {bulk_product.get_name_id()} -- debe venderse a granel para poder ser asociado."
            )

        if quantity.is_zero_or_less():
            return Result.failure(
                "La cantidad debe ser mayor a cero"
            )

        return Result.success(None)

    # ---------------------------------------------

    def get_name_id(self) -> ProductName:
        return self._product_name

    def get_bar_code(self) -> Optional[BarCode]:
        return self._bar_code

    def get_gain_amount(self) -> Money:
        return self._gain_amount

    def get_stock(self) -> ProductQuantity:
        return self._stock

    def get_reorder_level(self) -> Optional[ProductQuantity]:
        return self._reorder_level

    def get_gain_strategy(self) -> GainStrategy:
        return self._gain_strategy

    def get_sale_type(self) -> SaleType:
        return self._sale_type

    def get_category(self) -> Category:
        return self._category

    def get_registration_date(self) -> datetime:
        return self._registration_date

    def get_price(self) -> Money:
        return self._price