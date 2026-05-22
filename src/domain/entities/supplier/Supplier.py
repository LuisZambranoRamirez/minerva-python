from datetime import datetime
from typing import Final, Optional
from domain.entities.shared.PhoneNumber import PhoneNumber
from domain.entities.supplier.RUC import RUC
from domain.entities.supplier.SupplierId import SupplierId

class Supplier:
    def __init__(self, supplier_name: str, ruc: Optional[str] = None, phone_number: Optional[str] = None):
        self.supplier_name_id: Final[SupplierId] = SupplierId(supplier_name)
        self._ruc: Optional[RUC] = RUC(ruc) if ruc is not None else None
        self._phone_number: Optional[PhoneNumber] = PhoneNumber(phone_number) if phone_number is not None else None
        
        # VALORES POR DEFECTO
        self.registration_date: Final[datetime] = datetime.now()

    def update_phone_number(self, phone_number: Optional[str]) -> None:
        if phone_number is None:
            self._phone_number = None
            return

        self._phone_number = PhoneNumber(phone_number)

    def update_ruc(self, ruc: Optional[str]) -> None:
        if ruc is None:
            self._ruc = None
            return

        self._ruc = RUC(ruc)

    @property
    def ruc(self) -> Optional[RUC]:
        return self._ruc

    @property
    def phone_number(self) -> Optional[PhoneNumber]:
        return self._phone_number
