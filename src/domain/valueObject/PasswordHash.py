from domain.interfaces.ValueObject import ValueObject


class PasswordHash(ValueObject[str]):

    def __init__(self, value: str):
        super().__init__(value)