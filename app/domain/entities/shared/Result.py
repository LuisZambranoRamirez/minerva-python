from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


@dataclass(frozen=True)
class Result(Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None

    @staticmethod
    def success_result(data: T, message: str = "") -> "Result[T]":
        return Result(True, message, data)

    @staticmethod
    def fail(message: str = "") -> "Result[T]":
        return Result(False, message, None)

    def is_success(self) -> bool:
        return self.success

    def is_fail(self) -> bool:
        return not self.success

    def get_message(self) -> str:
        return self.message

    def get_data(self) -> Optional[T]:
        return self.data