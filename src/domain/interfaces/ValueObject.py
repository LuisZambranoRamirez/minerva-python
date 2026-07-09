from abc import ABC
from typing import Generic, TypeVar

from domain.exceptions.DomainException import DomainException


V = TypeVar("V")


class ValueObject(ABC, Generic[V]):
    def __init__(self, value: V):
        if value is None:
            raise DomainException("El valor no puede ser nulo.")

        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ValueObject):
            return False

        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)