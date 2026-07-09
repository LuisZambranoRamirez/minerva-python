from enum import Enum

class GainStrategyEnum(str, Enum):
    PORCENTAJE = "PORCENTAJE"
    INCREMENTAL = "INCREMENTAL"


class SaleTypeEnum(str, Enum):
    UNIDAD = "UNIDAD"
    GRANEL = "GRANEL"


class ProductCategoryEnum(str, Enum):
    BEBIDAS = "BEBIDAS"
    ABARROTES_SECOS = "ABARROTES_SECOS"
    CAFE_INFUSIONES = "CAFE_INFUSIONES"
    LACTEOS = "LACTEOS"
    CARNES = "CARNES"
    SNACKS_GOLOSINAS = "SNACKS_GOLOSINAS"
    CUIDADO_PERSONAL = "CUIDADO_PERSONAL"
    LIMPIEZA_HOGAR = "LIMPIEZA_HOGAR"
    BEBÉS = "BEBÉS"
    MASCOTAS = "MASCOTAS"
    OTROS = "OTROS"


class LossReasonEnum(str, Enum):
    DAÑADO = "DAÑADO"
    VENCIMIENTO = "VENCIMIENTO"
    PERDIDO = "PERDIDO"
    COMSUMO = "COMSUMO"
    ROBO = "ROBO"
    OTROS = "OTROS"


class PaymentMethodEnum(str, Enum):
    EFECTIVO = "EFECTIVO"
    DIGITAL = "DIGITAL"


class ReturnReasonEnum(str, Enum):
    DAÑADO = "DAÑADO"
    VENCIDO = "VENCIDO"
    EQUIVOCACION = "EQUIVOCACION"
    OTROS = "OTROS"