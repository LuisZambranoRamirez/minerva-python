from typing import List, Optional, Dict

from domain.entities.customer.Customer import Customer
from domain.entities.customer.CustomerId import CustomerId
from domain.repositories.CustomerRepository import CustomerRepository


class InMemoryCustomerRepository(CustomerRepository):
    def __init__(self):
        self._customers: Dict[str, Customer] = {}

    def save(self, customer: Customer) -> None:
        self._customers[customer.customer_id.value] = customer

    def exists_by_id(self, customer_id: CustomerId) -> bool:
        return customer_id.value in self._customers

    def find_all(self) -> List[Customer]:
        return list(self._customers.values())

    def find_by_id(self, customer_id: CustomerId) -> Optional[Customer]:
        return self._customers.get(customer_id.value)

    def delete_by_id(self, customer_id: CustomerId) -> None:
        if customer_id.value in self._customers:
            del self._customers[customer_id.value]
