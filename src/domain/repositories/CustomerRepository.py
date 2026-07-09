from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.customer.Customer import Customer
from domain.entities.customer.CustomerId import CustomerId
from domain.valueObject.PhoneNumber import PhoneNumber


class CustomerRepository(ABC):

    @abstractmethod
    def save(
        self,
        customer: Customer
    ) -> None:
        pass

    @abstractmethod
    def exists_by_id(
        self,
        id: CustomerId
    ) -> bool:
        pass

    @abstractmethod
    def exists_by_phone_number(
        self,
        phone_number: PhoneNumber
    ) -> bool:
        pass

    @abstractmethod
    def find_by_id(
        self,
        id: CustomerId
    ) -> Optional[Customer]:
        pass

    @abstractmethod
    def find_by_phone_number(
        self,
        phone_number: PhoneNumber
    ) -> Optional[Customer]:
        pass

    @abstractmethod
    def find_all(self) -> List[Customer]:
        pass