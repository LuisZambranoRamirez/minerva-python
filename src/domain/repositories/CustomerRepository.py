from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.customer.Customer import Customer
from domain.entities.customer.CustomerId import CustomerId
from domain.entities.shared.PhoneNumber import PhoneNumber


class CustomerRepository(ABC):

    @abstractmethod
    def save(self, customer: Customer) -> None:
        pass

    @abstractmethod
    def exists_by_id(self, customer_id: CustomerId) -> bool:
        pass

    @abstractmethod
    def find_all(self) -> List[Customer]:
        pass

    @abstractmethod
    def find_by_id(self, customer_id: CustomerId) -> Optional[Customer]:
        pass

    @abstractmethod
    def delete_by_id(self, customer_id: CustomerId) -> None:
        pass
