from datetime import datetime
from typing import Final, Optional
import uuid

from domain.exceptions.DomainException import DomainException 
from domain.entities.product.ProductId import ProductId
from domain.entities.product.ProductQuantity import ProductQuantity
from domain.entities.shared.Money import Money
from domain.entities.supplier.SupplierId import SupplierId

class StockEntry:
    def __init__(
        self,
        product_name_id: ProductId,
        supplier_name_id: SupplierId,
        price_unit: Money,
        quantity: ProductQuantity,
        expiration_date: Optional[datetime] = None
    ):
        # 1. Validaciones de presencia
        if product_name_id is None:
            raise DomainException("El nombre del producto no puede estar vacío.")
        if supplier_name_id is None:
            raise DomainException("El nombre del proveedor no puede estar vacío.")

        # 2. Validaciones de negocio sobre los objetos de valor
        if price_unit is not None and price_unit.is_zero_or_less():
            raise DomainException("El precio del producto debe ser mayor a 0.")
        if quantity is not None and quantity.is_zero_or_less():
            raise DomainException("La cantidad del producto debe ser mayor a 0.")

        # 3. Validación de consistencia de fechas temporales
        if expiration_date is not None and expiration_date <= datetime.now():
            raise DomainException(
                "La fecha de expiración debe ser posterior a la fecha actual."
            )

        # Asignación de propiedades de la entidad
        self.product_name_id: Final[ProductId] = product_name_id
        self.supplier_name_id: Final[SupplierId] = supplier_name_id
        self.price_unit: Final[Money] = price_unit
        self.quantity: Final[ProductQuantity] = quantity
        self.expiration_date: Final[Optional[datetime]] = expiration_date

        # DATOS POR DEFECTO AUTOMÁTICOS
        self.stock_entry_id: Final[uuid.UUID] = uuid.uuid4()
        self.registration_date: Final[datetime] = datetime.now()

    @property
    def id(self) -> uuid.UUID:
        return self.stock_entry_id

    # --------------------- EQUALS & HASH POR IDENTIDAD ---------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StockEntry):
            return False
        return self.stock_entry_id == other.stock_entry_id

    def __hash__(self) -> int:
        return hash(self.stock_entry_id)
