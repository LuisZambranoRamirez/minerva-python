from domain.entities.supplier.SupplierId import SupplierId
from domain.exceptions.DomainException import DomainException
from domain.valueObject.Name import Name


class SupplierName(Name, SupplierId):

    MIN_LENGTH = 3
    MAX_LENGTH = 100

    def __init__(self, value: str):
        super().__init__(
            value,
            self.MIN_LENGTH,
            self.MAX_LENGTH
        )

    def as_string(self) -> str:
        return self.value

    def get_value(self) -> str:
        return self.value