from abc import ABC, abstractmethod


class PasswordHasher(ABC):

    @abstractmethod
    def hash(self, raw_password: Password) -> PasswordHash:
        pass

    @abstractmethod
    def matches(self, password: str, hashed_password: PasswordHash) -> bool:
        pass