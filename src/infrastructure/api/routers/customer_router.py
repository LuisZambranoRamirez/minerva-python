from domain.repositories.UserRepository import UserRepository
from infrastructure.api.dependencies import get_customer_repository
from domain.repositories.CustomerRepository import CustomerRepository
from infrastructure.api.dependencies import get_user_repository
from infrastructure.api.dependencies import CurrentUser
from infrastructure.api.dependencies import get_current_user
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from application.services.CustomerService import CustomerService


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


# =========================
# DTO REQUESTS
# =========================

class RegisterCustomerRequest(BaseModel):
    customer_name: str
    phone_number: Optional[str] = None


class UpdatePhoneNumberRequest(BaseModel):
    phone_number: str

# =========================
# HELPER SERVICE
# =========================

def get_customer_service_with_user(
    current_user: CurrentUser = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
    customer_repository: CustomerRepository = Depends(get_customer_repository),
) -> CustomerService:

    return CustomerService(
        current_user.role,
        current_user.username,
        user_repository,
        customer_repository,
    )

# =========================
# WRITE ENDPOINTS
# =========================


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def register_customer(
    request: RegisterCustomerRequest,
    service: CustomerService = Depends(
        get_customer_service_with_user
    )
):
    result = service.register_customer(
        customer_name=request.customer_name,
        phone_number=request.phone_number,
    )

    if result.is_failure():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get_message(),
        )

    return {
        "message": "Cliente registrado correctamente."
    }


@router.put("/{customer_id}/phone")
def update_phone_number(
    customer_id: str,
    request: UpdatePhoneNumberRequest,
    service: CustomerService = Depends(
        get_customer_service_with_user
    ),
):

    result = service.update_phone_number(
        customer_id=customer_id,
        new_phone_number=request.phone_number,
    )

    if result.is_failure():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get_message(),
        )

    return {
        "message": "Número actualizado correctamente."
    }

# =========================
# READ ENDPOINTS
# =========================

@router.get("/{customer_id}")
def find_customer_by_id(
    customer_id: str,
    service: CustomerService = Depends(
        get_customer_service_with_user
    ),
):

    customer = service.find_customer_by_id(
        customer_id
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado.",
        )

    return customer

@router.get("/phone/{phone_number}")
def find_customer_by_phone_number(
    phone_number: str,
    service: CustomerService = Depends(
        get_customer_service_with_user
    ),
):

    customer = service.find_customer_by_phone_number(
        phone_number
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado.",
        )

    return customer

@router.get("")
def get_all_customers(
    service: CustomerService = Depends(
        get_customer_service_with_user
    ),
):

    return service.get_all_customers()