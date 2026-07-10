from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from application.services.SupplierService import SupplierService
from domain.repositories.SupplierRepository import SupplierRepository
from domain.repositories.UserRepository import UserRepository

from infrastructure.api.dependencies import (
    get_supplier_repository,
    get_user_repository,
    CurrentUser,
    get_current_user,
)


router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"],
)


# =========================
# DTO REQUESTS
# =========================

class RegisterSupplierRequest(BaseModel):
    supplier_name: str
    ruc: Optional[str] = None
    phone_number: Optional[str] = None


class UpdatePhoneNumberRequest(BaseModel):
    phone_number: str


class UpdateRucRequest(BaseModel):
    ruc: str



# =========================
# HELPER SERVICE
# =========================

def get_supplier_service_with_user(
    current_user: CurrentUser = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
    supplier_repository: SupplierRepository = Depends(
        get_supplier_repository
    ),
) -> SupplierService:

    return SupplierService(
        current_user.role,
        current_user.username,
        user_repository,
        supplier_repository,
    )



# =========================
# WRITE ENDPOINTS
# =========================


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def register_supplier(
    request: RegisterSupplierRequest,
    service: SupplierService = Depends(
        get_supplier_service_with_user
    )
):

    result = service.register(
        supplier_name=request.supplier_name,
        ruc=request.ruc,
        phone_number=request.phone_number,
    )


    if result.is_failure():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get_message(),
        )


    return {
        "message": "Proveedor registrado correctamente."
    }



@router.put("/{supplier_name}/phone")
def update_phone_number(
    supplier_name: str,
    request: UpdatePhoneNumberRequest,
    service: SupplierService = Depends(
        get_supplier_service_with_user
    ),
):

    result = service.update_phone_number(
        supplier_name=supplier_name,
        phone_number=request.phone_number,
    )


    if result.is_failure():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get_message(),
        )


    return {
        "message": "Número actualizado correctamente."
    }



@router.put("/{supplier_name}/ruc")
def update_ruc(
    supplier_name: str,
    request: UpdateRucRequest,
    service: SupplierService = Depends(
        get_supplier_service_with_user
    ),
):

    result = service.update_ruc(
        supplier_name=supplier_name,
        ruc=request.ruc,
    )


    if result.is_failure():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get_message(),
        )


    return {
        "message": "RUC actualizado correctamente."
    }



# =========================
# READ ENDPOINTS
# =========================


@router.get("/{supplier_name}")
def find_supplier_by_id(
    supplier_name: str,
    service: SupplierService = Depends(
        get_supplier_service_with_user
    ),
):

    supplier = service.find_by_id(
        supplier_name
    )


    if supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado.",
        )


    return supplier



@router.get("/ruc/{ruc}")
def find_supplier_by_ruc(
    ruc: str,
    service: SupplierService = Depends(
        get_supplier_service_with_user
    ),
):

    supplier = service.find_by_ruc(
        ruc
    )


    if supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado.",
        )


    return supplier



@router.get("/phone/{phone_number}")
def find_supplier_by_phone(
    phone_number: str,
    service: SupplierService = Depends(
        get_supplier_service_with_user
    ),
):

    supplier = service.find_by_phone(
        phone_number
    )


    if supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado.",
        )


    return supplier



@router.get("")
def get_all_suppliers(
    service: SupplierService = Depends(
        get_supplier_service_with_user
    ),
):

    return service.find_all()