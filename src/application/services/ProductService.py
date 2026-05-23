from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from domain.constants.Category import Category
from domain.constants.GainStrategy import GainStrategy
from domain.constants.SaleType import SaleType
from domain.entities.product.BarCode import BarCode
from domain.entities.product.ProductId import ProductId
from domain.entities.product.ProductQuantity import ProductQuantity
from domain.entities.product.Product import Product
from domain.repositories.ProductRepository import ProductRepository
from domain.repositories.SupplierRepository import SupplierRepository


class ProductService:  # Implementa conceptualmente ProductUseCase
    def __init__(
        self,
        product_repository: ProductRepository,
        supplier_repository: SupplierRepository
    ):
        self._product_repository = product_repository
        self._supplier_repository = supplier_repository

    def register_product(
        self,
        product_name: str,
        gain_strategy: GainStrategy,
        gain_amount: Decimal,
        reorder_level: Optional[Decimal],
        bar_code: Optional[str],
        sale_type: SaleType,
        category: Category
    ) -> None:
        """
        Registra un nuevo producto en el sistema validando restricciones de unicidad.
        Levanta ValueError si las reglas de negocio no se cumplen.
        """
        # La instanciación ejecuta todas las validaciones internas que antes hacía Product.create
        product_created = Product(
            product_name=product_name,
            gain_strategy=gain_strategy,
            gain_amount=gain_amount,
            sale_type=sale_type,
            category=category,
            reorder_level=reorder_level,
            bar_code=bar_code
        )

        # Validación de unicidad por ID (Nombre)
        if self._product_repository.exists_by_id(product_created.product_name_id):
            raise ValueError("Ya existe un producto con el mismo nombre.")

        # Validación de unicidad por Código de Barras si está presente
        if product_created.bar_code is not None:
            if self._product_repository.exists_by_bar_code(product_created.bar_code):
                raise ValueError("Ya existe un producto con el mismo código de barras.")

        self._product_repository.save_product(product_created)

    def register_stock_entry(
        self,
        product_id: str,
        supplier_name_id: str,
        price_unit: Decimal,
        quantity: Decimal,
        expiration_date: Optional[datetime] = None
    ) -> None:
        """Registra una entrada de stock para un producto existente."""
        product = self.find_product_by_id(product_id)
        if product is None:
            raise ValueError("El producto no está registrado.")

        # Genera el objeto de dominio StockEntry aplicando sus validaciones internas
        stock_entry = product.generate_stock_entry(
            supplier_name_id=supplier_name_id,
            price_unit=price_unit,
            quantity=quantity,
            expiration_date=expiration_date
        )

        self._product_repository.save_stock_entry(stock_entry)

    def register_unit_to_bulk(
        self,
        unit_product_id: str,
        bulk_product_id: str,
        quantity: Decimal
    ) -> None:
        """Asocia un producto vendido por unidades a su equivalente a granel."""
        unit_product = self.find_product_by_id(unit_product_id)
        if unit_product is None:
            raise ValueError("No se encontró el producto vendido por unidad.")

        bulk_product = self.find_product_by_id(bulk_product_id)
        if bulk_product is None:
            raise ValueError("No se encontró el producto vendido a granel.")

        # Instanciamos el Value Object de cantidad para la operación
        product_quantity = ProductQuantity(quantity)

        # Valida las reglas de asociación (levanta ValueError si falla)
        unit_product.validate_bulk_association(bulk_product, product_quantity)

        self._product_repository.save_unit_to_bulk(
            unit_product.product_name_id,
            bulk_product.product_name_id,
            product_quantity
        )

    def find_product_by_id(self, product_id: str) -> Optional[Product]:
        """Busca un producto por su identificador. Retorna None si no existe o es inválido."""
        try:
            # Si el string no pasa las validaciones de ProductId, se captura el error
            prod_id = ProductId(product_id)
            return self._product_repository.find_by_id(prod_id)
        except ValueError:
            return None

    def find_product_by_bar_code(self, bar_code: str) -> Optional[Product]:
        """Busca un producto por su código de barras. Retorna None si no existe o es inválido."""
        try:
            b_code = BarCode(bar_code)
            return self._product_repository.find_by_bar_code(b_code)
        except ValueError:
            return None

    def find_all_products(self) -> List[Product]:
        """Retorna la lista de todos los productos registrados."""
        return self._product_repository.find_all_products()