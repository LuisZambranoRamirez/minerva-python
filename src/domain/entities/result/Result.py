from typing import Generic, TypeVar, Optional


D = TypeVar("D")


class Result(Generic[D]):

    def __init__(
        self,
        success: bool,
        message: str,
        data: Optional[D]
    ):
        self._success = success
        self._message = message
        self._data = data

    @classmethod
    def success(cls, data: D, message: str = "") -> "Result[D]":
        return cls(True, message, data)

    @classmethod
    def failure(cls, message: str) -> "Result[D]":
        return cls(False, message, None)

    def is_success(self) -> bool:
        return self._success

    def is_failure(self) -> bool:
        return not self._success

    def get_message(self) -> str:
        return self._message

    def get_data(self) -> Optional[D]:
        return self._data