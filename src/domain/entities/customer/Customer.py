from datetime import datetime
from typing import Optional

from domain.entities.customer.CustomerId import CustomerId
from domain.entities.result.Result import Result
from domain.exceptions.DomainException import DomainException
from domain.exceptions.UnexpectedDomainException import UnexpectedDomainException
from domain.interfaces.Entity import Entity
from domain.valueObject.PhoneNumber import PhoneNumber
from domain.valueObject.id.CustomerName import CustomerName


class Customer(Entity[CustomerId]):

    def __init__(
        self,
        name: str,
        phone_number: Optional[str] = None
    ):
        try:
            temp_id = CustomerName(name)

            super().__init__(temp_id)

            self._customer_name = temp_id
            self._phone_number = (
                PhoneNumber(phone_number)
                if phone_number is not None
                else None
            )

            self._registration_date = datetime.now()

        except DomainException as e:
            raise UnexpectedDomainException(
                f"Error al crear el cliente: {str(e)}",
                e,
            )

    @classmethod
    def restore(
        cls,
        customer_name: str,
        registration_date: datetime,
        phone_number: Optional[str]
    ) -> "Customer":
        try:
            customer = cls.__new__(cls)

            temp_id = CustomerName(customer_name)

            Entity.__init__(customer, temp_id)

            customer._customer_name = temp_id
            customer._registration_date = registration_date
            customer._phone_number = (
                PhoneNumber(phone_number)
                if phone_number is not None
                else None
            )

            return customer

        except DomainException as e:
            raise UnexpectedDomainException(
                f"Error al crear el cliente: {str(e)}",
                e,
            )

    @property
    def customer_name(self) -> CustomerName:
        return self._customer_name

    @property
    def phone_number(self) -> Optional[PhoneNumber]:
        return self._phone_number

    def update_phone_number(
        self,
        new_phone_number: Optional[str]
    ) -> Result[None]:
        try:
            self._phone_number = (
                PhoneNumber(new_phone_number)
                if new_phone_number is not None
                else None
            )

        except DomainException as e:
            return Result.failure(str(e))

        return Result.success(None)

    @property
    def registration_date(self) -> datetime:
        return self._registration_date