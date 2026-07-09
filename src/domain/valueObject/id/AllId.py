from domain.interfaces.Id import Id


class AllId(Id[str]):

    def __init__(self):
        self._value = "ALL"

    def get_value(self) -> str:
        return self._value

    def as_string(self) -> str:
        return self._value