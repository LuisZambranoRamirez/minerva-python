from domain.entities.shared.Result import Result
from dataclasses import dataclass
import re


LENGTH = 9


@dataclass(frozen=True)
class PhoneNumber:
    value: str
    
    @staticmethod
    def of(value: str) -> Result["PhoneNumber"]:
        if value is None:
            return Result.fail("Ingrese un número de teléfono.")

        if len(value) != LENGTH:
            return Result.fail(
                f"El número de teléfono debe tener {LENGTH} dígitos."
            )

        if not re.fullmatch(r"\d+", value):
            return Result.fail(
                "El número de teléfono solo puede contener números."
            )

        return Result.success(PhoneNumber(value))