from pydantic import BaseModel
from typing import Optional


class SupplierCreate(BaseModel):
    supplier_name: str
    ruc: Optional[str] = None
    phone_number: Optional[str] = None


class SupplierUpdateRuc(BaseModel):
    ruc: str


class SupplierUpdatePhone(BaseModel):
    phone_number: str


class SupplierResponse(BaseModel):
    supplier_name: str
    ruc: Optional[str]
    phone_number: Optional[str]

    class Config:
        orm_mode = True
