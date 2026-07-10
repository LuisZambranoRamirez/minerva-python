from dataclasses import dataclass
from datetime import datetime
from domain.constants.PaymentMethod import PaymentMethod
from decimal import Decimal

class SaleItem:
    def __init__(
        self,
        product_id: str,
        quantity: Decimal,
        unit_price: Decimal
    ):
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price

class SaleDetailDTO:
    def __init__(
        self,
        sale_detail_id: str,
        product_id: str,
        quantity: Decimal,
        unit_price: Decimal
    ):
        self.sale_detail_id = sale_detail_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price

class PayDTO:
    def __init__(
        self,
        pay_id: str,
        amount: Decimal,
        payment_method: PaymentMethod,
        registration_date: datetime
    ):
        self.pay_id = pay_id
        self.amount = amount
        self.payment_method = payment_method
        self.registration_date = registration_date

@dataclass
class PayData:
    amount: Decimal
    payment_method: PaymentMethod