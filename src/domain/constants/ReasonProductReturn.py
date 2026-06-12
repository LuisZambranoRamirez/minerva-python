from enum import Enum


class ReasonProductReturn(str, Enum):
    DAÑADO = "DAÑADO"
    VENCIDO = "VENCIDO"
    EQUIVOCACION = "EQUIVOCACION"
    OTROS = "OTROS"
