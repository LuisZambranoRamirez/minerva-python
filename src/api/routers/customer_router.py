from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from application.services.CustomerService import CustomerService
from api.dependencies import get_customer_service
from api.schemas.CustomerSchema import CustomerCreate, CustomerResponse


router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_customer(
    customer_in: CustomerCreate,
    service: CustomerService = Depends(get_customer_service)
):
    try:
        service.register(
            customer_id=customer_in.customer_id,
            phone_number=customer_in.phone_number
        )
        return {"message": "Customer created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[CustomerResponse])
def get_customers(service: CustomerService = Depends(get_customer_service)):
    customers = service.find_all()
    return [
        CustomerResponse(
            customer_id=c.customer_id.value,
            phone_number=c.phone_number.value,
            registration_date=c.registration_date.isoformat()
        ) for c in customers
    ]

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: str, service: CustomerService = Depends(get_customer_service)):
    try:
        service.delete(customer_id)
    except ValueError as e:
        if "no encontrado" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
