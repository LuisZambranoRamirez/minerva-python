from typing import List, Optional

from domain.entities.shared.PhoneNumber import PhoneNumber
from domain.entities.supplier.RUC import RUC
from domain.entities.supplier.Supplier import Supplier
from domain.entities.supplier.SupplierId import SupplierId
from domain.repositories.SupplierRepository import SupplierRepository


class SupplierService:  # Implementa conceptualmente SupplierUseCase
    def __init__(self, supplier_repository: SupplierRepository):
        self._supplier_repository = supplier_repository

    # --------------------- ESCRITURA (COMMANDS) ---------------------

    def register(self, supplier_name: str, ruc: Optional[str], phone_number: Optional[str]) -> None:
        # La instanciación ejecuta todas las validaciones internas del dominio de manera directa
        supplier_created = Supplier(
            supplier_name=supplier_name,
            ruc=ruc,
            phone_number=phone_number
        )

        # 1. Validación de unicidad por ID de Proveedor
        if self._supplier_repository.exists_by_id(supplier_created.supplier_name_id):
            raise ValueError("Ya existe un proveedor con el mismo nombre.")

        # 2. Validación de unicidad por RUC (si viene informado)
        if supplier_created.ruc is not None:
            if self._supplier_repository.exists_by_ruc(supplier_created.ruc):
                raise ValueError("Ya existe un proveedor con el mismo RUC.")

        # 3. Validación de unicidad por Número de Teléfono (si viene informado)
        if supplier_created.phone_number is not None:
            if self._supplier_repository.exists_by_phone_number(supplier_created.phone_number):
                raise ValueError("Ya existe un proveedor con el mismo número de teléfono.")

        self._supplier_repository.save(supplier_created)

    def update_phone_number(self, supplier_name: str, phone_number: str) -> None:
        supplier = self.find_by_id(supplier_name)
        if supplier is None:
            raise ValueError("Proveedor no encontrado.")

        # El método mutador de la entidad valida internamente el formato usando el Value Object
        supplier.update_phone_number(phone_number)

        # Validación de unicidad posterior en la base de datos
        # (Asegúrate de que tu repositorio excluya al ID actual en entornos reales para evitar falsos positivos)
        if supplier.phone_number is not None and self._supplier_repository.exists_by_phone_number(supplier.phone_number):
            raise ValueError("Ya existe un proveedor con el mismo número de teléfono.")
        
        self._supplier_repository.save(supplier)

    def update_ruc(self, supplier_name: str, ruc: str) -> None:
        supplier = self.find_by_id(supplier_name)
        if supplier is None:
            raise ValueError("Proveedor no encontrado.")

        # La entidad muta su estado interno y valida la estructura del RUC
        supplier.update_ruc(ruc)

        if supplier.ruc is not None and self._supplier_repository.exists_by_ruc(supplier.ruc):
            raise ValueError("Ya existe un proveedor con el mismo RUC.")

        self._supplier_repository.save(supplier)

    # --------------------- LECTURA (QUERIES) ---------------------

    def find_all(self) -> List[Supplier]:
        return self._supplier_repository.find_all()

    def find_by_id(self, supplier_name: str) -> Optional[Supplier]:
        try:
            supplier_id = SupplierId(supplier_name)
            return self._supplier_repository.find_by_id(supplier_id)
        except ValueError:
            return None

    def find_by_ruc(self, ruc: str) -> Optional[Supplier]:
        try:
            ruc_vo = RUC(ruc)
            return self._supplier_repository.find_by_ruc(ruc_vo)
        except ValueError:
            return None

    def find_by_phone_number(self, phone: str) -> Optional[Supplier]:
        try:
            phone_vo = PhoneNumber(phone)
            return self._supplier_repository.find_by_phone_number(phone_vo)
        except ValueError:
            return None
