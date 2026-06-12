from pydantic import BaseModel


class CustomerCreate(BaseModel):
    customer_id: str
    phone_number: str


class CustomerUpdatePhone(BaseModel):
    phone_number: str


class CustomerResponse(BaseModel):
    customer_id: str
    phone_number: str
    registration_date: str

    class Config:
        orm_mode = True
