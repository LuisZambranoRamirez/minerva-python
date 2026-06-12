from domain.exceptions.DomainException import DomainException

class MinimumAmountException(DomainException):
    def __init__(self, min_amount, cause=None):
        mensaje = f"El monto no puede ser menor que {min_amount}."
        super().__init__(mensaje)
