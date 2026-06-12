from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from application.services.ProductService import ProductService
from api.dependencies import get_product_service
from api.schemas.ProductSchema import ProductCreate, ProductResponse


router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    service: ProductService = Depends(get_product_service)
):
    try:
        service.register_product(
            product_name=product_in.product_name,
            gain_strategy=product_in.gain_strategy,
            gain_amount=product_in.gain_amount,
            reorder_level=product_in.reorder_level,
            bar_code=product_in.bar_code,
            sale_type=product_in.sale_type,
            category=product_in.category
        )
        return {"message": "Product created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[ProductResponse])
def get_products(service: ProductService = Depends(get_product_service)):
    products = service.find_all_products()
    return [
        ProductResponse(
            product_name=p.product_name_id.value,
            gain_strategy=p.gain_strategy.value,
            gain_amount=float(p.gain_amount),
            sale_type=p.sale_type.value,
            category=p.category.value,
            reorder_level=float(p.reorder_level) if p.reorder_level else None,
            bar_code=p.bar_code.value if p.bar_code else None
        ) for p in products
    ]

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str, service: ProductService = Depends(get_product_service)):
    # ProductService originally doesn't have delete, but our UI requires it.
    # We will invoke the repo directly through the service if we added it, or directly here.
    # Since we didn't add delete to ProductService, let's just use the repo
    from api.dependencies import product_repo
    from domain.entities.product.ProductId import ProductId
    try:
        p_id = ProductId(product_id)
        if not product_repo.exists_by_id(p_id):
            raise HTTPException(status_code=404, detail="Product not found")
        product_repo.delete_by_id(p_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Product ID")
