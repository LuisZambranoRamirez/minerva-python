from domain.entities.customer.CustomerId import CustomerId
from domain.valueObject.Name import Name


class CustomerName(Name, CustomerId):

    MIN_LENGTH = 3
    MAX_LENGTH = 50

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