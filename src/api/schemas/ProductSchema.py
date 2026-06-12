from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

from domain.constants.Category import Category
from domain.constants.GainStrategy import GainStrategy
from domain.constants.SaleType import SaleType


class ProductCreate(BaseModel):
    product_name: str
    gain_strategy: GainStrategy
    gain_amount: Decimal
    sale_type: SaleType
    category: Category
    reorder_level: Optional[Decimal] = None
    bar_code: Optional[str] = None


class ProductResponse(BaseModel):
    product_name: str
    gain_strategy: str
    gain_amount: float
    sale_type: str
    category: str
    reorder_level: Optional[float]
    bar_code: Optional[str]

    class Config:
        orm_mode = True
