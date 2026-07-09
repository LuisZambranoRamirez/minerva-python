# infra/api/routers/supplier_router.py

from fastapi import APIRouter, Depends, HTTPException, status

from application.services.SupplierService import SupplierService
from infra.api.dependencies import get_supplier_service
from infra.api.dto.supplier_request import (
    RegisterSupplierRequest,
    UpdatePhoneRequest,
    UpdateRucRequest,
)

router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"],
)

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def register_supplier(
    request: RegisterSupplierRequest,
    service: SupplierService = Depends(get_supplier_service),
):
    result = service.register(
        supplier_name=request.supplier_name,
        ruc=request.ruc,
        phone_number=request.phone_number,
    )

    if result.is_failure():
        raise HTTPException(400, detail=result.error)

    return {
        "message": "Proveedor registrado correctamente."
    }

@router.put("/{supplier_name}/phone")
def update_phone(
    supplier_name: str,
    request: UpdatePhoneRequest,
    service: SupplierService = Depends(get_supplier_service),
):
    result = service.update_phone_number(
        supplier_name=supplier_name,
        phone_number=request.phone_number,
    )

    if result.is_failure():
        raise HTTPException(400, detail=result.error)

    return {
        "message": "Teléfono actualizado correctamente."
    }

@router.put("/{supplier_name}/ruc")
def update_ruc(
    supplier_name: str,
    request: UpdateRucRequest,
    service: SupplierService = Depends(get_supplier_service),
):
    result = service.update_ruc(
        supplier_name=supplier_name,
        ruc=request.ruc,
    )

    if result.is_failure():
        raise HTTPException(400, detail=result.error)

    return {
        "message": "RUC actualizado correctamente."
    }

@router.get("/{supplier_name}")
def find_by_id(
    supplier_name: str,
    service: SupplierService = Depends(get_supplier_service),
):
    supplier = service.find_by_id(supplier_name)

    if supplier is None:
        raise HTTPException(
            status_code=404,
            detail="Proveedor no encontrado.",
        )

    return supplier

@router.get("/ruc/{ruc}")
def find_by_ruc(
    ruc: str,
    service: SupplierService = Depends(get_supplier_service),
):
    supplier = service.find_by_ruc(ruc)

    if supplier is None:
        raise HTTPException(
            status_code=404,
            detail="Proveedor no encontrado.",
        )

    return supplier

@router.get("/phone/{phone_number}")
def find_by_phone(
    phone_number: str,
    service: SupplierService = Depends(get_supplier_service),
):
    supplier = service.find_by_phone(phone_number)

    if supplier is None:
        raise HTTPException(
            status_code=404,
            detail="Proveedor no encontrado.",
        )

    return supplier

@router.get("")
def find_all(
    service: SupplierService = Depends(get_supplier_service),
):
    return service.find_all()