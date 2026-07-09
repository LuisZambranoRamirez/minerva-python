from datetime import datetime

from domain.constants.ReasonProductReturn import ReasonProductReturn
from domain.entities.sale.ProductReturnId import ProductReturnId
from domain.exceptions.DomainException import DomainException
from domain.interfaces.Entity import Entity
from domain.valueObject.ProductQuantity import ProductQuantity
from domain.valueObject.id.ProductReturnIdImpl import ProductReturnIdImpl


class ProductReturn(Entity[ProductReturnId]):

    def __init__(
        self,
        quantity: ProductQuantity,
        reason: ReasonProductReturn
    ):
        if (
            quantity is not None
            and quantity.is_zero_or_less()
        ):
            raise DomainException(
                "La cantidad a devolver debe ser mayor a cero."
            )

        if reason is None:
            raise DomainException(
                "La razón de la devolución no puede estar vacío."
            )

        super().__init__(
            ProductReturnIdImpl.generate()
        )

        self._quantity = quantity
        self._reason = reason
        self._registration_date = datetime.now()

    @property
    def quantity(self) -> ProductQuantity:
        return self._quantity

    @property
    def reason(self) -> ReasonProductReturn:
        return self._reason

    @property
    def registration_date(self) -> datetime:
        return self._registration_date