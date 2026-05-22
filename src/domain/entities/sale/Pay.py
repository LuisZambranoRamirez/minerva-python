from datetime import datetime
from decimal import Decimal
from typing import Final
import uuid

from domain.constants.PaymentMethod import PaymentMethod
from domain.entities.shared.Money import Money

class Pay:
    MIN_AMOUNT: Final[Decimal] = Decimal("0.10")

    def __init__(self, amount: Money, payment_method: PaymentMethod):
        # 1. Validaciones de presencia y negocio
        if payment_method is None:
            raise ValueError("El método de pago no puede estar vacío.")
            
        if amount is None:
            raise ValueError("El monto no puede estar vacío.")
            
        if amount.value < self.MIN_AMOUNT:
            raise ValueError(f"El MONTO debe ser mayor o igual a S/{self.MIN_AMOUNT}")

        # 2. Asignación de propiedades de la entidad (Inmutables en este caso)
        self.amount: Final[Money] = amount
        self.payment_method: Final[PaymentMethod] = payment_method

        # VALORES POR DEFECTO AUTOMÁTICOS
        self.pay_id: Final[uuid.UUID] = uuid.uuid4()
        self.registration_date: Final[datetime] = datetime.now()

    @property
    def id(self) -> uuid.UUID:
        return self.pay_id

    # --------------------- EQUALS & HASH POR IDENTIDAD ---------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pay):
            return False
        return self.pay_id == other.pay_id

    def __hash__(self) -> int:
        return hash(self.pay_id)
