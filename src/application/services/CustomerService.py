from typing import List, Optional

from domain.entities.customer.Customer import Customer
from domain.entities.customer.CustomerId import CustomerId
from domain.repositories.CustomerRepository import CustomerRepository


class CustomerService:
    def __init__(self, customer_repository: CustomerRepository):
        self._customer_repository = customer_repository

    def register(self, customer_id: str, phone_number: str) -> None:
        customer_created = Customer(
            customer_id=customer_id,
            phone_number=phone_number
        )

        if self._customer_repository.exists_by_id(customer_created.customer_id):
            raise ValueError("Ya existe un cliente con el mismo nombre/ID.")

        self._customer_repository.save(customer_created)

    def find_all(self) -> List[Customer]:
        return self._customer_repository.find_all()

    def find_by_id(self, customer_id_str: str) -> Optional[Customer]:
        try:
            c_id = CustomerId(customer_id_str)
            return self._customer_repository.find_by_id(c_id)
        except ValueError:
            return None

    def update(self, customer_id: str, new_phone_number: str) -> None:
        customer = self.find_by_id(customer_id)
        if customer is None:
            raise ValueError("Cliente no encontrado.")

        # Recreamos el cliente o actualizamos el nro. En el modelo original no hay un mutador
        # 'update_phone_number'. Así que podemos simplemente crear una nueva instancia
        # o asignarle un nuevo PhoneNumber si decidimos mutar. 
        # Dado que Customer no tiene setters definidos, lo recrearemos asumiendo la fecha actual o similar,
        # o preferiblemente, modificaremos los atributos si lo consideramos Entity. 
        # Pero como esto es solo en memoria para el frontend...
        from domain.entities.shared.PhoneNumber import PhoneNumber
        customer._phone_number = PhoneNumber(new_phone_number)

        self._customer_repository.save(customer)

    def delete(self, customer_id: str) -> None:
        try:
            c_id = CustomerId(customer_id)
            if not self._customer_repository.exists_by_id(c_id):
                raise ValueError("Cliente no encontrado.")
            self._customer_repository.delete_by_id(c_id)
        except ValueError as e:
            raise ValueError(str(e))
