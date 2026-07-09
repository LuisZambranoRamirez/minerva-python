from typing import Optional

from application.services.Service import Service
from domain.constants.Permission import Permission
from domain.constants.Role import Role
from domain.entities.customer.Customer import Customer
from domain.entities.result.Result import Result
from domain.exceptions.DomainException import DomainException
from domain.exceptions.UnauthorizedActionException import (
    UnauthorizedActionException,
)
from domain.repositories.CustomerRepository import CustomerRepository
from domain.repositories.UserRepository import UserRepository
from domain.valueObject.PhoneNumber import PhoneNumber
from domain.valueObject.id.AllId import AllId
from domain.valueObject.id.CustomerName import CustomerName
from domain.valueObject.id.UserName import UserName


class CustomerService(Service):

    def __init__(
        self,
        user_role: Role,
        user_name: UserName,
        user_repository: UserRepository,
        customer_repository: CustomerRepository,
    ):
        super().__init__(
            user_role,
            user_name,
            user_repository,
        )
        self._customer_repository = customer_repository

    # --------------------- WRITE ---------------------

    def register_customer(
        self,
        customer_name: str,
        phone_number: Optional[str],
    ) -> Result[None]:

        if self.get_user_role.lacks_permission(
            Permission.CUSTOMER_REGISTER
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para registrar clientes."
            )

        try:
            customer = Customer(
                customer_name,
                phone_number,
            )

            if self._customer_repository.exists_by_id(
                customer.customer_name
            ):
                return Result.failure(
                    "Ya existe un cliente con el mismo nombre."
                )

            if (
                customer.phone_number is not None
                and self._customer_repository.exists_by_phone_number(
                    customer.phone_number
                )
            ):
                return Result.failure(
                    "Ya existe un cliente con el mismo número de teléfono."
                )

            self._customer_repository.save(customer)

        except DomainException as e:
            return Result.failure(str(e))

        self._register_user_action(
            Permission.CUSTOMER_REGISTER,
            customer.id,
        )

        return Result.success(None)

    def update_phone_number(
        self,
        customer_id: str,
        new_phone_number: str,
    ) -> Result[None]:

        if self.get_user_role.lacks_permission(
            Permission.CUSTOMER_UPDATE_PHONE_NUMBER
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para actualizar el número de teléfono del cliente."
            )

        try:
            customer = self._customer_repository.find_by_id(
                CustomerName(customer_id)
            )

            if customer is None:
                return Result.failure(
                    "Cliente no encontrado."
                )

            result = customer.update_phone_number(
                new_phone_number
            )

            if result.is_failure():
                return result

            if self._customer_repository.exists_by_phone_number(
                PhoneNumber(new_phone_number)
            ):
                return Result.failure(
                    "Ya existe un cliente con el mismo número de teléfono."
                )

            self._customer_repository.save(customer)

            self._register_user_action(
                Permission.CUSTOMER_UPDATE_PHONE_NUMBER,
                customer.id,
            )

            return Result.success(None)

        except DomainException:
            return Result.failure(
                "Cliente no encontrado."
            )

    # --------------------- READ ---------------------

    def find_customer_by_id(
        self,
        customer_id: str,
    ) -> Optional[Customer]:

        if self.get_user_role.lacks_permission(
            Permission.CUSTOMER_FIND_BY_ID
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para buscar clientes por ID."
            )

        try:
            customer_name = CustomerName(customer_id)

            self._register_user_action(
                Permission.CUSTOMER_FIND_BY_ID,
                customer_name,
            )

            return self._customer_repository.find_by_id(
                customer_name
            )

        except DomainException:
            return None

    def find_customer_by_phone_number(
        self,
        phone_number: str,
    ) -> Optional[Customer]:

        if self.get_user_role.lacks_permission(
            Permission.CUSTOMER_FIND_BY_PHONE_NUMBER
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para buscar clientes por número de teléfono."
            )

        try:
            customer = (
                self._customer_repository.find_by_phone_number(
                    PhoneNumber(phone_number)
                )
            )

            if customer is not None:
                self._register_user_action(
                    Permission.CUSTOMER_FIND_BY_PHONE_NUMBER,
                    customer.id,
                )

            return customer

        except DomainException:
            return None

    def get_all_customers(
        self,
    ) -> list[Customer]:

        if self.get_user_role.lacks_permission(
            Permission.CUSTOMER_GET_ALL
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para obtener todos los clientes."
            )

        customers = self._customer_repository.find_all()

        self._register_user_action(
            Permission.CUSTOMER_GET_ALL,
            AllId(),
        )

        return customers