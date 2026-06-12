from enum import Enum


class ReasonProductLoss(str, Enum):
    DAÑADO = "DAÑADO"
    VENCIMIENTO = "VENCIMIENTO"
    PERDIDO = "PERDIDO"
    CONSUMO = "CONSUMO"
    DRAKO = "DRAKO"
    ROBO = "ROBO"
    OTROS = "OTROS"
