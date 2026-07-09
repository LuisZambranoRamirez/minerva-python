from datetime import datetime
from typing import Optional

from domain.entities.result.Result import Result
from domain.entities.supplier.SupplierId import SupplierId
from domain.exceptions.DomainException import DomainException
from domain.exceptions.UnexpectedDomainException import UnexpectedDomainException
from domain.interfaces.Entity import Entity
from domain.valueObject.PhoneNumber import PhoneNumber
from domain.valueObject.RUC import RUC
from domain.valueObject.id.SupplierName import SupplierName


class Supplier(Entity[SupplierId]):

    def __init__(
        self,
        supplier_name: str,
        ruc: Optional[str],
        phone_number: Optional[str],
    ):
        temp_id = SupplierName(supplier_name)

        super().__init__(temp_id)

        self._supplier_name = temp_id
        self._ruc = RUC(ruc) if ruc is not None else None
        self._phone_number = (
            PhoneNumber(phone_number)
            if phone_number is not None
            else None
        )

        self._registration_date = datetime.now()

    @classmethod
    def restore(
        cls,
        supplier_name: str,
        ruc: Optional[str],
        phone_number: Optional[str],
        registration_date: datetime,
    ) -> "Supplier":

        try:
            supplier = cls.__new__(cls)

            temp_id = SupplierName(supplier_name)

            Entity.__init__(supplier, temp_id)

            supplier._supplier_name = temp_id
            supplier._registration_date = registration_date
            supplier._ruc = (
                RUC(ruc)
                if ruc is not None
                else None
            )
            supplier._phone_number = (
                PhoneNumber(phone_number)
                if phone_number is not None
                else None
            )

            return supplier

        except DomainException as e:
            raise UnexpectedDomainException(
                f"Error al crear el proveedor: {str(e)}",
                e,
            )

    # -------------------------------------

    def update_phone_number(
        self,
        phone_number: Optional[str],
    ) -> Result[None]:

        try:
            self._phone_number = (
                PhoneNumber(phone_number)
                if phone_number is not None
                else None
            )

        except DomainException as e:
            return Result.failure(str(e))

        return Result.success(None)

    def update_ruc(
        self,
        ruc: Optional[str],
    ) -> Result[None]:

        try:
            self._ruc = (
                RUC(ruc)
                if ruc is not None
                else None
            )

        except DomainException as e:
            return Result.failure(str(e))

        return Result.success(None)

    # -------------------------------------

    @property
    def supplier_name(self) -> SupplierName:
        return self._supplier_name

    @property
    def registration_date(self) -> datetime:
        return self._registration_date

    @property
    def ruc(self) -> Optional[RUC]:
        return self._ruc

    @property
    def phone_number(self) -> Optional[PhoneNumber]:
        return self._phone_number