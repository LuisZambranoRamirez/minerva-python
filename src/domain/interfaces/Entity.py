from domain.interfaces.Id import Id
from domain.exceptions.UnexpectedDomainException import UnexpectedDomainException
from abc import ABC
from typing import Generic, TypeVar


I = TypeVar("I", bound=Id)


class Entity(ABC, Generic[I]):
    def __init__(self, id: I):
        if id is None:
            raise UnexpectedDomainException("El ID no puede ser nulo")
        self._id = id

    @property
    def id(self) -> I:
        return self._id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False

        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)