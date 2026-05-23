from decimal import Decimal
from typing import Final
import uuid

from domain.exceptions.domainException import DomainException 
from domain.entities.product.ProductId import ProductId
from domain.entities.product.ProductQuantity import ProductQuantity
from domain.entities.shared.Money import Money

class SaleDetail:
    def __init__(self, product_id: ProductId, quantity: ProductQuantity, price_unit: Money):
        # 1. Validaciones de presencia y reglas de negocio
        if product_id is None:
            raise DomainException("El PRODUCTO es requerido.")
            
        if quantity is None:
            raise DomainException("La CANTIDAD DE PRODUCTO no puede estar vacía.")
        if quantity.is_zero_or_less():
            raise DomainException("La CANTIDAD DE PRODUCTO debe ser mayor a 0.")
            
        if price_unit is None:
            raise DomainException("El PRECIO UNITARIO no puede estar vacío.")
        if price_unit.is_zero_or_less():
            raise DomainException("El PRECIO UNITARIO debe ser mayor a 0.")

        # 2. Asignación de propiedades (Inmutables)
        self.product_name_id: Final[ProductId] = product_id
        self.quantity: Final[ProductQuantity] = quantity
        self.price_unit: Final[Money] = price_unit

        # Identificador único de la entidad generado automáticamente
        self._id: Final[uuid.UUID] = uuid.uuid4()

    def calculate_total(self) -> Decimal:
        """Calcula el subtotal multiplicando el precio unitario por la cantidad."""
        return self.price_unit.value * self.quantity.value

    @property
    def id(self) -> uuid.UUID:
        return self._id

    # --------------------- EQUALS & HASH POR IDENTIDAD ---------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SaleDetail):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)
