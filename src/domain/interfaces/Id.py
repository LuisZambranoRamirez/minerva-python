from abc import ABC, abstractmethod
from typing import Generic, TypeVar


I = TypeVar("I")


class Id(ABC, Generic[I]):
    @abstractmethod
    def value(self) -> I:
        pass

    @abstractmethod
    def as_string(self) -> str:
        pass