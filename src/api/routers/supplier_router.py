from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from application.services.SupplierService import SupplierService
from api.dependencies import get_supplier_service
from api.schemas.SupplierSchema import SupplierCreate, SupplierResponse


router = APIRouter(prefix="/suppliers", tags=["suppliers"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_supplier(
    supplier_in: SupplierCreate,
    service: SupplierService = Depends(get_supplier_service)
):
    try:
        service.register(
            supplier_name=supplier_in.supplier_name,
            ruc=supplier_in.ruc,
            phone_number=supplier_in.phone_number
        )
        return {"message": "Supplier created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[SupplierResponse])
def get_suppliers(service: SupplierService = Depends(get_supplier_service)):
    suppliers = service.find_all()
    return [
        SupplierResponse(
            supplier_name=s.supplier_name_id.value,
            ruc=s.ruc.value if s.ruc else None,
            phone_number=s.phone_number.value if s.phone_number else None
        ) for s in suppliers
    ]

@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: str):
    from api.dependencies import supplier_repo
    from domain.entities.supplier.SupplierId import SupplierId
    try:
        s_id = SupplierId(supplier_id)
        if not supplier_repo.exists_by_id(s_id):
            raise HTTPException(status_code=404, detail="Supplier not found")
        supplier_repo.delete_by_id(s_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Supplier ID")
