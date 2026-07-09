# infra/api/routers/customer_router.py

from fastapi import APIRouter, Depends, HTTPException, status
# infra/api/dto/customer_request.py

from typing import Optional

from pydantic import BaseModel
from application.services.CustomerService import CustomerService
from domain.exceptions.UnauthorizedActionException import UnauthorizedActionException

from infra.api.dependencies import get_customer_service
from infra.api.dto.customer_request import (
    RegisterCustomerRequest,
    UpdatePhoneNumberRequest,
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def register_customer(
    request: RegisterCustomerRequest,
    service: CustomerService = Depends(get_customer_service),
):
    try:
        result = service.register_customer(
            customer_name=request.customer_name,
            phone_number=request.phone_number,
        )

        if result.is_failure():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.error,
            )

        return {
            "message": "Cliente registrado correctamente."
        }

    except UnauthorizedActionException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    
@router.put("/{customer_id}/phone")
def update_phone_number(
    customer_id: str,
    request: UpdatePhoneNumberRequest,
    service: CustomerService = Depends(get_customer_service),
):
    try:
        result = service.update_phone_number(
            customer_id=customer_id,
            new_phone_number=request.phone_number,
        )

        if result.is_failure():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.error,
            )

        return {
            "message": "Número actualizado correctamente."
        }

    except UnauthorizedActionException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    
@router.get("/{customer_id}")
def find_customer_by_id(
    customer_id: str,
    service: CustomerService = Depends(get_customer_service),
):
    try:
        customer = service.find_customer_by_id(customer_id)

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado.",
            )

        return customer

    except UnauthorizedActionException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )

@router.get("/phone/{phone_number}")
def find_customer_by_phone_number(
    phone_number: str,
    service: CustomerService = Depends(get_customer_service),
):
    try:
        customer = service.find_customer_by_phone_number(phone_number)

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado.",
            )

        return customer

    except UnauthorizedActionException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    
@router.get("")
def get_all_customers(
    service: CustomerService = Depends(get_customer_service),
):
    try:
        return service.get_all_customers()

    except UnauthorizedActionException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    



class RegisterCustomerRequest(BaseModel):
    customer_name: str
    phone_number: Optional[str] = None


class UpdatePhoneNumberRequest(BaseModel):
    phone_number: str