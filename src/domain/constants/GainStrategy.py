from enum import Enum


class GainStrategy(str, Enum):
    PORCENTAJE = "PORCENTAJE"
    INCREMENTAL = "INCREMENTAL"
