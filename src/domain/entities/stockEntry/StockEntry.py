from datetime import datetime
from decimal import Decimal
from typing import Optional

from domain.entities.stockEntry.StockEntryId import StockEntryId
from domain.exceptions.DomainException import DomainException
from domain.exceptions.UnexpectedDomainException import UnexpectedDomainException
from domain.interfaces.Entity import Entity
from domain.valueObject.Money import Money
from domain.valueObject.ProductQuantity import ProductQuantity
from domain.valueObject.id.ProductName import ProductName
from domain.valueObject.id.StockEntryIdImpl import StockEntryIdImpl
from domain.valueObject.id.SupplierName import SupplierName


class StockEntry(Entity[StockEntryId]):

    def __init__(
        self,
        product_name: str,
        supplier_name: str,
        unit_price: Decimal,
        quantity: Decimal,
        expiration_date: Optional[datetime],
    ):
        super().__init__(StockEntryIdImpl.generate())

        self._product_name = ProductName(product_name)
        self._supplier_name = SupplierName(supplier_name)
        self._unit_price = Money(unit_price)
        self._quantity = ProductQuantity(quantity)

        if self._unit_price.is_zero_or_less():
            raise DomainException(
                "El precio del producto debe ser mayor a 0."
            )

        if self._quantity.is_zero_or_less():
            raise DomainException(
                "La cantidad del producto debe ser mayor a 0."
            )

        if (
            expiration_date is not None
            and expiration_date <= datetime.now()
        ):
            raise DomainException(
                "La fecha de expiración debe ser posterior a la fecha actual."
            )

        self._expiration_date = expiration_date
        self._registration_date = datetime.now()

    @classmethod
    def restore(
        cls,
        stock_entry_id: str,
        product_name: str,
        supplier_name: str,
        unit_price: Decimal,
        quantity: Decimal,
        expiration_date: Optional[datetime],
        registration_date: datetime,
    ) -> "StockEntry":

        try:
            stock_entry = cls.__new__(cls)

            temp_id = StockEntryIdImpl.from_string(
                stock_entry_id
            )

            Entity.__init__(
                stock_entry,
                temp_id
            )

            stock_entry._product_name = ProductName(
                product_name
            )

            stock_entry._supplier_name = SupplierName(
                supplier_name
            )

            stock_entry._unit_price = Money(
                unit_price
            )

            stock_entry._quantity = ProductQuantity(
                quantity
            )

            stock_entry._expiration_date = expiration_date
            stock_entry._registration_date = registration_date

            return stock_entry

        except DomainException as e:
            raise UnexpectedDomainException(
                f"Error al crear la entrada de stock: {str(e)}",
                e,
            )

    # -------------------------------------

    @property
    def product_name(self) -> ProductName:
        return self._product_name

    @property
    def supplier_name(self) -> SupplierName:
        return self._supplier_name

    @property
    def unit_price(self) -> Money:
        return self._unit_price

    @property
    def quantity(self) -> ProductQuantity:
        return self._quantity

    @property
    def expiration_date(self) -> Optional[datetime]:
        return self._expiration_date

    @property
    def registration_date(self) -> datetime:
        return self._registration_date