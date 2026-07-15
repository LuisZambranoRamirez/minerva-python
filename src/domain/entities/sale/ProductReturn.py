from datetime import datetime

from domain.constants.ReasonProductReturn import ReasonProductReturn
from domain.entities.sale.ProductReturnId import ProductReturnId
from domain.exceptions.DomainException import DomainException
from domain.interfaces.Entity import Entity
from domain.valueObject.ProductQuantity import ProductQuantity
from domain.valueObject.id.ProductName import ProductName
from domain.valueObject.id.ProductReturnIdImpl import ProductReturnIdImpl


class ProductReturn(Entity[ProductReturnId]):

    def __init__(
        self,
        product_name: ProductName,
        quantity: ProductQuantity,
        reason: ReasonProductReturn,
        sale_detail_id: str | None = None
    ):
        if product_name is None:
            raise DomainException(
                "El nombre del producto no puede estar vacío."
            )

        if (
            quantity is not None
            and quantity.is_zero_or_less()
        ):
            raise DomainException(
                "La cantidad a devolver debe ser mayor a cero."
            )

        if reason is None:
            raise DomainException(
                "La razón de la devolución no puede estar vacía."
            )

        super().__init__(
            ProductReturnIdImpl.generate()
        )

        self._product_name = product_name
        self._quantity = quantity
        self._reason = reason
        self._sale_detail_id = sale_detail_id
        self._registration_date = datetime.now()

    @property
    def product_name(self) -> ProductName:
        return self._product_name

    @property
    def quantity(self) -> ProductQuantity:
        return self._quantity

    @property
    def reason(self) -> ReasonProductReturn:
        return self._reason

    @property
    def sale_detail_id(self) -> str | None:
        return self._sale_detail_id

    @property
    def registration_date(self) -> datetime:
        return self._registration_date