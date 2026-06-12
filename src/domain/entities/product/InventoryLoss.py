from datetime import datetime
from typing import Final, Optional
import uuid

from domain.exceptions.DomainException import DomainException 
from domain.constants.ReasonProductLoss import ReasonProductLoss
from domain.entities.product.ProductId import ProductId
from domain.entities.product.ProductQuantity import ProductQuantity

class InventoryLoss:
    def __init__(
        self,
        product_name_id: ProductId,
        quantity: ProductQuantity,
        reason: ReasonProductLoss,
        observation: Optional[str] = None
    ):
        # 1. Validaciones de presencia y consistencia
        if product_name_id is None:
            raise DomainException("El nombre del producto no puede estar vacío.")
        
        if quantity is not None and quantity.is_zero_or_less():
            raise DomainException("La cantidad debe ser mayor a cero.")
            
        if reason is None:
            raise DomainException("Debe especificar la razón de la pérdida.")

        # 2. Asignación de propiedades inmutables (Final)
        self.product_name_id: Final[ProductId] = product_name_id
        self.quantity: Final[ProductQuantity] = quantity
        self.registration_date: Final[datetime] = datetime.now()
        self.inventory_loss_id: Final[uuid.UUID] = uuid.uuid4()

        # 3. Asignación de propiedades mutables
        self._reason: ReasonProductLoss = reason
        self._observation: Optional[str] = observation

    @property
    def id(self) -> uuid.UUID:
        return self.inventory_loss_id

    # --------------------- PROPIEDADES MUTABLES (GETTERS / SETTERS) ---------------------

    @property
    def reason(self) -> ReasonProductLoss:
        return self._reason

    @reason.setter
    def reason(self, value: ReasonProductLoss) -> None:
        if value is None:
            raise DomainException("Debe especificar una razón de pérdida válida.")
        self._reason = value

    @property
    def observation(self) -> Optional[str]:
        return self._observation

    @observation.setter
    def observation(self, value: Optional[str]) -> None:
        self._observation = value

    # --------------------- EQUALS & HASH POR IDENTIDAD ---------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, InventoryLoss):
            return False
        return self.inventory_loss_id == other.inventory_loss_id

    def __hash__(self) -> int:
        return hash(self.inventory_loss_id)
