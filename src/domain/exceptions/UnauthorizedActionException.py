from domain.exceptions.DomainException import DomainException

class UnauthorizedActionException(DomainException):
    def __init__(self, message: str):
        super().__init__(message)