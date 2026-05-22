from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


@dataclass(frozen=True)
class Result(Generic[T]):
    is_success: bool
    message: str
    data: Optional[T] = None

    @staticmethod
    def success(data: T, message: str = "") -> "Result[T]":
        return Result(True, message, data)

    @staticmethod
    def fail(message: str = "") -> "Result[T]":
        return Result(False, message, None)