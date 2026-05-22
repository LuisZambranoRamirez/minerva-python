from datetime import datetime
from typing import Final, Optional
import uuid

from domain.constants.ReasonProductReturn import ReasonProductReturn
from domain.entities.product.ProductQuantity import ProductQuantity

class ProductReturn:
    def __init__(self, quantity: ProductQuantity, reason: ReasonProductReturn):
        # 1. Validaciones de presencia y lógica de negocio
        if quantity is None:
            raise ValueError("La cantidad a devolver no puede estar vacía.")
            
        if quantity.is_zero_or_less():
            raise ValueError("La cantidad a devolver debe ser mayor a cero.")
            
        if reason is None:
            raise ValueError("La razón de la devolución no puede estar vacía.")

        # 2. Asignación de propiedades (Inmutables)
        self.quantity: Final[ProductQuantity] = quantity
        self.reason: Final[ReasonProductReturn] = reason

        # VALORES POR DEFECTO AUTOMÁTICOS
        self.product_return_id: Final[uuid.UUID] = uuid.uuid4()
        self.registration_date: Final[datetime] = datetime.now()

    @property
    def id(self) -> uuid.UUID:
        return self.product_return_id

    # --------------------- EQUALS & HASH POR IDENTIDAD ---------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ProductReturn):
            return False
        return self.product_return_id == other.product_return_id

    def __hash__(self) -> int:
        return hash(self.product_return_id)
