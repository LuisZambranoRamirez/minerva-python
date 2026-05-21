from enum import Enum


class PaymentMethod(str, Enum):
    EFECTIVO = "EFECTIVO"
    DIGITAL = "DIGITAL"