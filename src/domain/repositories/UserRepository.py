from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.user.User import User
from domain.entities.user.UserId import UserId
from domain.entities.userAction.UserAction import UserAction
from domain.valueObject.DNI import DNI


class UserRepository(ABC):

    @abstractmethod
    def save(
        self,
        user: User
    ) -> None:
        pass

    @abstractmethod
    def save_user_action(
        self,
        user_action: UserAction
    ) -> None:
        pass

    @abstractmethod
    def exists_by_id(
        self,
        id: UserId
    ) -> bool:
        pass

    @abstractmethod
    def exists_by_dni(
        self,
        dni: DNI
    ) -> bool:
        pass

    @abstractmethod
    def find_by_id(
        self,
        id: UserId
    ) -> Optional[User]:
        pass