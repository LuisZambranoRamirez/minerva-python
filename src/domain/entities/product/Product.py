from datetime import datetime
from decimal import Decimal
from typing import Final, Optional

from domain.exceptions.domainException import DomainException 
from domain.constants.GainStrategy import GainStrategy
from domain.constants.Category import Category
from domain.constants.SaleType import SaleType
from domain.entities.product.BarCode import BarCode
from domain.entities.product.ProductId import ProductId
from domain.entities.product.ProductQuantity import ProductQuantity
from domain.entities.product.StockEntry import StockEntry
from domain.entities.shared.Money import Money
from domain.entities.supplier.SupplierId import SupplierId
from domain.services.math import Math  


class Product:
    def __init__(
        self,
        product_name: str,
        gain_strategy: GainStrategy,
        gain_amount: Decimal,
        sale_type: SaleType,
        category: Category,
        reorder_level: Optional[Decimal] = None,
        bar_code: Optional[str] = None
    ):
        # 1. Validaciones de presencia para Enums obligatorios
        if gain_strategy is None:
            raise DomainException("Seleccione una estrategia de ganancia.")
        if sale_type is None:
            raise DomainException("Seleccione el tipo de venta.")
        if category is None:
            raise DomainException("Seleccione una categoría.")

        # 2. Inicialización y validación de los Value Objects base
        self.product_name_id: Final[ProductId] = ProductId(product_name)
        
        gain_money = Money(gain_amount)
        if gain_money.is_zero_or_less():
            raise DomainException("El monto de ganancia debe ser mayor a cero.")
        self._gain_amount: Money = gain_money

        # 3. Validación y asignación del nivel de reposición (Reorder Level)
        self._reorder_level: Optional[ProductQuantity] = None
        if reorder_level is not None:
            reorder_qty = ProductQuantity(reorder_level)
            if sale_type == SaleType.UNIDAD and Math.is_decimal(reorder_qty.value):
                raise DomainException(
                    "El nivel de reposición no puede ser decimal para productos vendidos por unidad."
                )
            self._reorder_level = reorder_qty

        # 4. Validación y asignación del Código de Barras (Obligatorio solo si es por Unidad)
        self._bar_code: Optional[BarCode] = None
        if sale_type == SaleType.UNIDAD:
            if bar_code is None:
                raise DomainException("Ingrese el código de barras para productos vendidos por unidad.")
            self._bar_code = BarCode(bar_code)

        # 5. Estado inicial y valores por defecto automáticos
        self._stock: ProductQuantity = ProductQuantity.zero()
        self._gain_strategy: GainStrategy = gain_strategy
        self._sale_type: SaleType = sale_type
        self.category: Final[Category] = category
        self.registration_date: Final[datetime] = datetime.now()

    # --------------------- OPERACIONES DE STOCK ---------------------

    def increase_stock(self, quantity_to_add: Decimal) -> None:
        if quantity_to_add is None:
            raise DomainException("La cantidad a sumar no puede ser nula.")
        
        new_stock_value = self._stock.value + quantity_to_add
        self._update_stock(new_stock_value)

    def decrease_stock(self, quantity_to_subtract: Decimal) -> None:
        if quantity_to_subtract is None:
            raise DomainException("La cantidad a restar no puede ser nula.")
            
        new_stock_value = self._stock.value - quantity_to_subtract
        if new_stock_value < 0:
            raise DomainException("No hay stock suficiente para realizar esta operación.")
            
        self._update_stock(new_stock_value)

    def _update_stock(self, new_stock_value: Decimal) -> None:
        new_stock = ProductQuantity(new_stock_value)
        
        if self._sale_type == SaleType.UNIDAD and Math.is_decimal(new_stock.value):
            raise DomainException("Este producto se maneja por unidades. Ingrese una cantidad entera.")
            
        self._stock = new_stock

    # --------------------- LÓGICA DE NEGOCIO ---------------------

    def validate_bulk_association(self, bulk_product: "Product", quantity: ProductQuantity) -> None:
        if bulk_product is None:
            raise DomainException("El producto a granel no puede ser nulo.")
        if quantity is None:
            raise DomainException("La cantidad no puede estar vacía.")

        if self == bulk_product:
            raise DomainException("No es posible asociar un producto consigo mismo.")
        if self._sale_type != SaleType.UNIDAD:
            raise DomainException(
                f"El producto -- {self.product_name_id} -- se vende por unidad y no permite asociar otro producto."
            )
        if bulk_product.sale_type != SaleType.GRANEL:
            raise DomainException(
                f"El producto -- {bulk_product.product_name_id} -- debe venderse a granel para poder ser asociado."
            )
        if quantity.is_zero_or_less():
            raise DomainException("La cantidad debe ser mayor a cero.")

    def generate_stock_entry(
        self, 
        supplier_name_id: str, 
        price_unit: Decimal, 
        quantity: Decimal, 
        expiration_date: Optional[datetime] = None
    ) -> StockEntry:
        # Las validaciones estructurales de los parámetros ocurren al instanciar cada Value Object
        supplier_id = SupplierId(supplier_name_id)
        money_price = Money(price_unit)
        qty_product = ProductQuantity(quantity)

        return StockEntry(
            product_name_id=self.product_name_id,
            supplier_name_id=supplier_id,
            price_unit=money_price,
            quantity=qty_product,
            expiration_date=expiration_date
        )

    # --------------------- PROPIEDADES (GETTERS / SETTERS) ---------------------

    @property
    def stock(self) -> ProductQuantity:
        return self._stock

    @property
    def gain_strategy(self) -> GainStrategy:
        return self._gain_strategy

    @property
    def gain_amount(self) -> Money:
        return self._gain_amount

    @property
    def sale_type(self) -> SaleType:
        return self._sale_type

    @property
    def bar_code(self) -> Optional[BarCode]:
        return self._bar_code

    @property
    def reorder_level(self) -> Optional[ProductQuantity]:
        return self._reorder_level

    # --------------------- EQUALS & HASH POR IDENTIDAD ---------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Product):
            return False
        return self.product_name_id == other.product_name_id

    def __hash__(self) -> int:
        return hash(self.product_name_id)
