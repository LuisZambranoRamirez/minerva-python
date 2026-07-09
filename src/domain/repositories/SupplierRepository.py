from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.supplier.Supplier import Supplier
from domain.entities.supplier.SupplierId import SupplierId
from domain.valueObject.PhoneNumber import PhoneNumber
from domain.valueObject.RUC import RUC


class SupplierRepository(ABC):

    @abstractmethod
    def save(
        self,
        supplier: Supplier
    ) -> None:
        pass

    @abstractmethod
    def exists_by_id(
        self,
        id: SupplierId
    ) -> bool:
        pass

    @abstractmethod
    def exists_by_ruc(
        self,
        ruc: RUC
    ) -> bool:
        pass

    @abstractmethod
    def exists_by_phone_number(
        self,
        phone_number: PhoneNumber
    ) -> bool:
        pass

    @abstractmethod
    def find_all(self) -> List[Supplier]:
        pass

    @abstractmethod
    def find_by_id(
        self,
        id: SupplierId
    ) -> Optional[Supplier]:
        pass

    @abstractmethod
    def find_by_ruc(
        self,
        ruc: RUC
    ) -> Optional[Supplier]:
        pass

    @abstractmethod
    def find_by_phone(
        self,
        phone_number: PhoneNumber
    ) -> Optional[Supplier]:
        pass