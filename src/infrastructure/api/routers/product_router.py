from decimal import Decimal
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from domain.constants.Category import Category
from domain.constants.GainStrategy import GainStrategy
from domain.constants.SaleType import SaleType

from domain.repositories.UserRepository import UserRepository
from domain.repositories.ProductRepository import ProductRepository
from domain.repositories.SupplierRepository import SupplierRepository

from infrastructure.api.dependencies import (
    get_user_repository,
    get_product_repository,
    get_supplier_repository,
    CurrentUser,
    get_current_user,
)

from application.services.ProductService import ProductService


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


# =========================
# DTO REQUESTS
# =========================


class RegisterProductRequest(BaseModel):
    product_name: str
    gain_strategy: GainStrategy
    gain_amount: Decimal
    reorder_level: Optional[Decimal] = None
    bar_code: Optional[str] = None
    sale_type: SaleType
    category: Category
    purchased_from_supplier_id: str
    purchase_unit_price: Decimal
    purchase_quantity: Decimal
    purchase_expiration_date: datetime



class RegisterStockEntryRequest(BaseModel):
    product_name: str
    supplier_name: str
    unit_price: Decimal
    quantity: Decimal
    expiration_date: datetime



# =========================
# HELPER SERVICE
# =========================


def get_product_service_with_user(
    current_user: CurrentUser = Depends(get_current_user),
    user_repository: UserRepository = Depends(
        get_user_repository
    ),
    product_repository: ProductRepository = Depends(
        get_product_repository
    ),
    supplier_repository: SupplierRepository = Depends(
        get_supplier_repository
    ),
) -> ProductService:

    return ProductService(
        current_user.role,
        current_user.username,
        user_repository,
        product_repository,
        supplier_repository,
    )



# =========================
# WRITE ENDPOINTS
# =========================


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def register_product(
    request: RegisterProductRequest,
    service: ProductService = Depends(
        get_product_service_with_user
    ),
):

    result = service.register_product(
        product_name=request.product_name,
        gain_strategy=request.gain_strategy,
        gain_amount=request.gain_amount,
        reorder_level=request.reorder_level,
        bar_code=request.bar_code,
        sale_type=request.sale_type,
        category=request.category,
        purchased_from_supplier_id=request.purchased_from_supplier_id,
        purchase_unit_price=request.purchase_unit_price,
        purchase_quantity=request.purchase_quantity,
        purchase_expiration_date=request.purchase_expiration_date,
    )


    if result.is_failure():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get_message(),
        )


    return {
        "message": "Producto registrado correctamente."
    }



@router.post(
    "/stock-entry",
    status_code=status.HTTP_201_CREATED
)
def register_stock_entry(
    request: RegisterStockEntryRequest,
    service: ProductService = Depends(
        get_product_service_with_user
    ),
):

    result = service.register_stock_entry(
        product_name=request.product_name,
        supplier_name=request.supplier_name,
        unit_price=request.unit_price,
        quantity=request.quantity,
        expiration_date=request.expiration_date,
    )


    if result.is_failure():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get_message(),
        )


    return {
        "message": "Entrada de stock registrada correctamente."
    }



# =========================
# READ ENDPOINTS
# =========================


@router.get("/{product_id}")
def find_product_by_id(
    product_id: str,
    service: ProductService = Depends(
        get_product_service_with_user
    ),
):

    product = service.find_product_by_id(
        product_id
    )


    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado.",
        )


    return product



@router.get("/barcode/{bar_code}")
def find_product_by_bar_code(
    bar_code: str,
    service: ProductService = Depends(
        get_product_service_with_user
    ),
):

    product = service.find_product_by_bar_code(
        bar_code
    )


    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado.",
        )


    return product



@router.get("")
def find_all_products(
    service: ProductService = Depends(
        get_product_service_with_user
    ),
):

    return service.find_all_products()