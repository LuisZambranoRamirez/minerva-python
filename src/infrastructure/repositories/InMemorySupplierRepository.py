from typing import List, Optional, Dict

from domain.entities.supplier.Supplier import Supplier
from domain.entities.supplier.SupplierId import SupplierId
from domain.entities.supplier.RUC import RUC
from domain.entities.shared.PhoneNumber import PhoneNumber
from domain.repositories.SupplierRepository import SupplierRepository


class InMemorySupplierRepository(SupplierRepository):
    def __init__(self):
        self._suppliers: Dict[str, Supplier] = {}

    def save(self, supplier: Supplier) -> None:
        self._suppliers[supplier.supplier_name_id.value] = supplier

    def exists_by_id(self, supplier_id: SupplierId) -> bool:
        return supplier_id.value in self._suppliers

    def exists_by_ruc(self, ruc: RUC) -> bool:
        return any(s.ruc and s.ruc.value == ruc.value for s in self._suppliers.values())

    def exists_by_phone_number(self, phone_number: PhoneNumber) -> bool:
        return any(s.phone_number and s.phone_number.value == phone_number.value for s in self._suppliers.values())

    def find_all(self) -> List[Supplier]:
        return list(self._suppliers.values())

    def find_by_id(self, supplier_id: SupplierId) -> Optional[Supplier]:
        return self._suppliers.get(supplier_id.value)

    def find_by_ruc(self, ruc: RUC) -> Optional[Supplier]:
        for s in self._suppliers.values():
            if s.ruc and s.ruc.value == ruc.value:
                return s
        return None

    def find_by_phone_number(self, phone_number: PhoneNumber) -> Optional[Supplier]:
        for s in self._suppliers.values():
            if s.phone_number and s.phone_number.value == phone_number.value:
                return s
        return None

    def delete_by_id(self, supplier_id: SupplierId) -> None:
        if supplier_id.value in self._suppliers:
            del self._suppliers[supplier_id.value]
