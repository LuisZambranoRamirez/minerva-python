from domain.constants.PaymentMethod import PaymentMethod
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from decimal import Decimal
from datetime import datetime

from domain.entities.sale.DTO import SaleItem, PayData

from domain.repositories.UserRepository import UserRepository
from domain.repositories.SaleRepository import SaleRepository
from domain.repositories.CustomerRepository import CustomerRepository
from domain.repositories.ProductRepository import ProductRepository

from infrastructure.api.dependencies import (
    CurrentUser,
    get_current_user,
    get_user_repository,
    get_sale_repository,
    get_customer_repository,
    get_product_repository,
)

from application.services.SaleService import SaleService


router = APIRouter(
    prefix="/sales",
    tags=["Sales"],
)


# =========================
# DTO REQUESTS
# =========================


class SaleItemRequest(BaseModel):
    product_id: str
    quantity: Decimal
    unit_price: Decimal


class PayDataRequest(BaseModel):
    payment_type: PaymentMethod
    amount: Decimal


class RegisterSaleRequest(BaseModel):
    customer_id: str
    pays: PayDataRequest
    items: list[SaleItemRequest]



class AddPaymentRequest(BaseModel):
    pays: PayDataRequest



# =========================
# HELPER SERVICE
# =========================


def get_sale_service_with_user(
    current_user: CurrentUser = Depends(get_current_user),
    user_repository: UserRepository = Depends(
        get_user_repository
    ),
    sale_repository: SaleRepository = Depends(
        get_sale_repository
    ),
    customer_repository: CustomerRepository = Depends(
        get_customer_repository
    ),
    product_repository: ProductRepository = Depends(
        get_product_repository
    ),
) -> SaleService:

    return SaleService(
        current_user.role,
        current_user.username,
        user_repository,
        sale_repository,
        customer_repository,
        product_repository,
    )



# =========================
# WRITE ENDPOINTS
# =========================


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def register_sale(
    request: RegisterSaleRequest,
    service: SaleService = Depends(
        get_sale_service_with_user
    ),
):

    pays = PayData(
            amount=request.pays.amount,
            payment_method=request.pays.payment_type
        )
    


    items = [
        SaleItem(
            product_id=i.product_id,
            quantity=i.quantity,
            unit_price=i.unit_price
        )
        for i in request.items
    ]


    result = service.register_sale(
        customer_id=request.customer_id,
        pays=pays,
        items=items,
    )


    if result.is_failure():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get_message(),
        )


    return {
        "message": "Venta registrada correctamente."
    }



@router.post(
    "/{sale_id}/payments"
)
def add_payment_to_sale(
    sale_id: str,
    request: AddPaymentRequest,
    service: SaleService = Depends(
        get_sale_service_with_user
    ),
):

    pays = PayData(
            payment_method=request.pays.payment_type,
            amount=request.pays.amount
        )
        


    result = service.add_payment_to_sale(
        sale_id_str=sale_id,
        pays=pays,
    )


    if result.is_failure():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get_message(),
        )


    return {
        "message": "Pago agregado correctamente."
    }



# =========================
# READ ENDPOINTS
# =========================


@router.get("/{sale_id}")
def find_sale_by_id(
    sale_id: str,
    service: SaleService = Depends(
        get_sale_service_with_user
    ),
):

    sale = service.find_sale_by_id(
        sale_id
    )


    if sale is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada.",
        )


    return sale



@router.get("/customer/{customer_id}")
def find_sales_by_customer_id(
    customer_id: str,
    service: SaleService = Depends(
        get_sale_service_with_user
    ),
):

    sales = service.find_sales_by_customer_id(
        customer_id
    )


    return sales



@router.get("")
def find_all_sales(
    service: SaleService = Depends(
        get_sale_service_with_user
    ),
):

    return service.find_all_sales()