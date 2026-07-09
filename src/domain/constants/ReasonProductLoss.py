from enum import Enum


class ReasonProductLoss(str, Enum):
    DAÑADO = "DAÑADO"
    VENCIMIENTO = "VENCIMIENTO"
    PERDIDO = "PERDIDO"
    CONSUMO = "CONSUMO"
    ROBO = "ROBO"
    OTROS = "OTROS"