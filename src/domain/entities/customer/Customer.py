from domain.entities.shared.PhoneNumber import PhoneNumber
from domain.entities.customer.CustomerId import CustomerId
from datetime import datetime


class Customer:
    def __init__(self, customer_id: str, phone_number: str):
        self._customer_id: CustomerId = CustomerId(customer_id)
        self._phone_number: PhoneNumber = PhoneNumber(phone_number)
        self._registration_date: datetime = datetime.now()

    @property
    def customer_id(self) -> CustomerId:
        return self._customer_id

    @property
    def phone_number(self) -> PhoneNumber:
        return self._phone_number

    @property
    def registration_date(self) -> datetime:
        return self._registration_date

    def __eq__(self, other) -> bool:
        if not isinstance(other, Customer):
            return False
        return self._customer_id == other._customer_id

    def __hash__(self) -> int:
        return hash(self._customer_id)