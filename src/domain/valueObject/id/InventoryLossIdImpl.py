from uuid import UUID, uuid4

from domain.entities.product.InventoryLossId import InventoryLossId
from domain.exceptions.DomainException import DomainException
from domain.exceptions.UnexpectedDomainException import UnexpectedDomainException
from domain.interfaces.ValueObject import ValueObject


class InventoryLossIdImpl(ValueObject[UUID], InventoryLossId):

    def __init__(self, value: UUID):
        super().__init__(value)

    @classmethod
    def generate(cls) -> "InventoryLossIdImpl":
        try:
            return cls(uuid4())

        except DomainException as e:
            raise UnexpectedDomainException(
                f"Error al generar el ID de pérdida de inventario: {str(e)}",
                e,
            )

    @classmethod
    def from_string(cls, value: str) -> "InventoryLossIdImpl":
        try:
            return cls(UUID(value))

        except ValueError:
            raise DomainException(
                f"El ID de pérdida de inventario no tiene un formato válido: {value}"
            )

        except Exception as e:
            raise UnexpectedDomainException(
                str(e),
                e,
            )

    def as_string(self) -> str:
        return str(self.value)

    def get_value(self) -> UUID:
        return self.value