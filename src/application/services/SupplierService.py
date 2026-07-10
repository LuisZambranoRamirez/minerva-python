from typing import Optional

from application.services.Service import Service
from domain.constants.Permission import Permission
from domain.constants.Role import Role
from domain.entities.result.Result import Result
from domain.entities.supplier.Supplier import Supplier
from domain.exceptions.DomainException import DomainException
from domain.exceptions.UnauthorizedActionException import (
    UnauthorizedActionException,
)
from domain.repositories.SupplierRepository import SupplierRepository
from domain.repositories.UserRepository import UserRepository
from domain.valueObject.PhoneNumber import PhoneNumber
from domain.valueObject.RUC import RUC
from domain.valueObject.id.AllId import AllId
from domain.valueObject.id.SupplierName import SupplierName
from domain.valueObject.id.UserName import UserName


class SupplierService(Service):

    def __init__(
        self,
        user_role: Role,
        user_name: UserName,
        user_repository: UserRepository,
        supplier_repository: SupplierRepository,
    ):
        super().__init__(
            user_role,
            user_name,
            user_repository,
        )

        self._supplier_repository = supplier_repository

    # --------------------- WRITE ---------------------

    def register(
        self,
        supplier_name: str,
        ruc: Optional[str],
        phone_number: Optional[str],
    ) -> Result[None]:

        if self.get_user_role.lacks_permission(
            Permission.SUPPLIER_REGISTER
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para registrar proveedores."
            )

        try:
            supplier = Supplier(
                supplier_name,
                ruc,
                phone_number,
            )

        except DomainException as e:
            return Result.failure(str(e))

        if self._supplier_repository.exists_by_id(
            supplier.supplier_name
        ):
            return Result.failure(
                "Ya existe un proveedor con el mismo nombre."
            )

        if (
            supplier.ruc is not None
            and self._supplier_repository.exists_by_ruc(
                supplier.ruc
            )
        ):
            return Result.failure(
                "Ya existe un proveedor con el mismo RUC."
            )

        if (
            supplier.phone_number is not None
            and self._supplier_repository.exists_by_phone_number(
                supplier.phone_number
            )
        ):
            return Result.failure(
                "Ya existe un proveedor con el mismo número de teléfono."
            )

        self._supplier_repository.save(supplier)

        self._register_user_action(
            Permission.SUPPLIER_REGISTER,
            supplier.id,
        )

        return Result.success(None)

    def update_phone_number(
        self,
        supplier_name: str,
        phone_number: str,
    ) -> Result[None]:

        if self.get_user_role.lacks_permission(
            Permission.SUPPLIER_UPDATE_PHONE_NUMBER
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para actualizar el número de teléfono del proveedor."
            )

        supplier = self.find_by_id(supplier_name)

        if supplier is None:
            return Result.failure(
                "Proveedor no encontrado."
            )

        result = supplier.update_phone_number(
            phone_number
        )

        if result.is_failure():
            return result

        if (
            supplier.phone_number is not None
            and self._supplier_repository.exists_by_phone_number(
                supplier.phone_number
            )
        ):
            return Result.failure(
                "Ya existe un proveedor con el mismo número de teléfono."
            )

        self._supplier_repository.save(supplier)

        self._register_user_action(
            Permission.SUPPLIER_UPDATE_PHONE_NUMBER,
            supplier.id,
        )

        return Result.success(None)

    def update_ruc(
        self,
        supplier_name: str,
        ruc: str,
    ) -> Result[None]:

        if self.get_user_role.lacks_permission(
            Permission.SUPPLIER_UPDATE_RUC
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para actualizar el RUC del proveedor."
            )

        supplier = self.find_by_id(supplier_name)

        if supplier is None:
            return Result.failure(
                "Proveedor no encontrado."
            )

        result = supplier.update_ruc(ruc)

        if result.is_failure():
            return result

        if (
            supplier.ruc is not None
            and self._supplier_repository.exists_by_ruc(
                supplier.ruc
            )
        ):
            return Result.failure(
                "Ya existe un proveedor con el mismo RUC."
            )

        self._supplier_repository.save(supplier)

        self._register_user_action(
            Permission.SUPPLIER_UPDATE_RUC,
            supplier.id,
        )

        return Result.success(None)

    # --------------------- READ ---------------------

    def find_all(self) -> list[Supplier]:

        if self.get_user_role.lacks_permission(
            Permission.SUPPLIER_FIND_ALL
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para buscar todos los proveedores."
            )

        suppliers = self._supplier_repository.find_all()

        self._register_user_action(
            Permission.SUPPLIER_FIND_ALL,
            AllId(),
        )

        return suppliers

    def find_by_id(
        self,
        supplier_name: str,
    ) -> Optional[Supplier]:

        if self.get_user_role.lacks_permission(
            Permission.SUPPLIER_FIND_BY_ID
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para buscar proveedores por ID."
            )

        try:
            supplier_name_obj = SupplierName(
                supplier_name
            )

            self._register_user_action(
                Permission.SUPPLIER_FIND_BY_ID,
                supplier_name_obj,
            )

            return self._supplier_repository.find_by_id(
                supplier_name_obj
            )

        except DomainException:
            return None

    def find_by_ruc(
        self,
        ruc: str,
    ) -> Optional[Supplier]:

        if self._user_role.lacks_permission(
            Permission.SUPPLIER_FIND_BY_RUC
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para buscar proveedores por RUC."
            )

        try:
            supplier = self._supplier_repository.find_by_ruc(
                RUC(ruc)
            )

            if supplier is not None:
                self._register_user_action(
                    Permission.SUPPLIER_FIND_BY_RUC,
                    supplier.id,
                )

            return supplier

        except DomainException:
            return None

    def find_by_phone(
        self,
        phone_number: str,
    ) -> Optional[Supplier]:

        if self._user_role.lacks_permission(
            Permission.SUPPLIER_UPDATE_PHONE_NUMBER
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para buscar proveedores por teléfono."
            )

        try:
            supplier = self._supplier_repository.find_by_phone(
                PhoneNumber(phone_number)
            )

            if supplier is not None:
                self._register_user_action(
                    Permission.SUPPLIER_UPDATE_PHONE_NUMBER,
                    supplier.id,
                )

            return supplier

        except DomainException:
            return None