from datetime import datetime
from typing import Optional

from domain.constants.ReasonProductLoss import ReasonProductLoss
from domain.entities.product.InventoryLossId import InventoryLossId
from domain.exceptions.DomainException import DomainException
from domain.interfaces.Entity import Entity
from domain.valueObject.ProductQuantity import ProductQuantity
from domain.valueObject.id.InventoryLossIdImpl import InventoryLossIdImpl
from domain.valueObject.id.ProductName import ProductName


class InventoryLoss(Entity[InventoryLossId]):

    def __init__(
        self,
        product_name: ProductName,
        quantity: ProductQuantity,
        reason: ReasonProductLoss,
        observation: Optional[str]
    ):
        if product_name is None:
            raise DomainException(
                "El nombre del producto no puede estar vacío."
            )

        if quantity is not None and quantity.is_zero_or_less():
            raise DomainException(
                "La cantidad debe ser mayor a cero."
            )

        if reason is None:
            raise DomainException(
                "Debe especificar la razón de la pérdida."
            )

        super().__init__(InventoryLossIdImpl.generate())

        self._product_name = product_name
        self._quantity = quantity
        self._reason = reason
        self._observation = observation
        self._registration_date = datetime.now()

    @property
    def product_name(self) -> ProductName:
        return self._product_name

    @property
    def quantity(self) -> ProductQuantity:
        return self._quantity

    @property
    def observation(self) -> Optional[str]:
        return self._observation

    @property
    def reason(self) -> ReasonProductLoss:
        return self._reason

    @property
    def registration_date(self) -> datetime:
        return self._registration_date