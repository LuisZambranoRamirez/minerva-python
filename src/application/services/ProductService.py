from decimal import Decimal
from datetime import datetime
from typing import Optional

from domain.constants.Category import Category
from domain.constants.GainStrategy import GainStrategy
from domain.constants.Permission import Permission
from domain.constants.Role import Role
from domain.constants.SaleType import SaleType
from domain.entities.product.Product import Product
from domain.entities.stockEntry.StockEntry import StockEntry
from domain.entities.result.Result import Result
from domain.exceptions.DomainException import DomainException
from domain.exceptions.UnauthorizedActionException import UnauthorizedActionException
from domain.repositories.ProductRepository import ProductRepository
from domain.repositories.SupplierRepository import SupplierRepository
from domain.repositories.UserRepository import UserRepository
from domain.valueObject.BarCode import BarCode
from domain.valueObject.ProductQuantity import ProductQuantity
from domain.valueObject.id.AllId import AllId
from domain.valueObject.id.ProductName import ProductName
from domain.valueObject.id.UserName import UserName
from application.services.Service import Service


class ProductService(Service):

    def __init__(
        self,
        user_role: Role,
        user_name: UserName,
        user_repository: UserRepository,
        product_repository: ProductRepository,
        supplier_repository: SupplierRepository
    ):
        super().__init__(
            user_role,
            user_name,
            user_repository
        )

        self._product_repository = product_repository
        self._supplier_repository = supplier_repository


    # --------------------- WRITE ---------------------

    def register_product(
        self,
        product_name: str,
        gain_strategy: GainStrategy,
        gain_amount: Decimal,
        reorder_level: Optional[Decimal],
        bar_code: Optional[str],
        sale_type: SaleType,
        category: Category,
        purchased_from_supplier_id: str,
        purchase_unit_price: Decimal,
        purchase_quantity: Decimal,
        purchase_expiration_date: datetime
    ) -> Result[None]:

        if self.get_user_role.lacks_permission(
            Permission.PRODUCT_REGISTER
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para registrar productos."
            )

        try:
            product_created = Product(
                product_name,
                gain_strategy,
                gain_amount,
                reorder_level,
                bar_code,
                sale_type,
                purchase_quantity,
                category,
                purchase_unit_price
            )

            stock_entry_created = StockEntry(
                product_name,
                purchased_from_supplier_id,
                purchase_unit_price,
                purchase_quantity,
                purchase_expiration_date
            )

        except DomainException as e:
            return Result.failure(str(e))


        if self._product_repository.exists_by_id(
            product_created.get_name_id()
        ):
            return Result.failure(
                "Ya existe un producto con el mismo nombre."
            )


        product_bar_code = product_created.get_bar_code()

        if (
            product_bar_code is not None
            and self._product_repository.exists_by_bar_code(
                product_bar_code
            )
        ):
            return Result.failure(
                "Ya existe un producto con el mismo código de barras."
            )


        if not self._supplier_repository.exists_by_id(
            stock_entry_created.supplier_name
        ):
            return Result.failure(
                "El proveedor no esta registrado."
            )


        self._product_repository.register_product(
            product_created,
            stock_entry_created
        )


        self._register_user_action(
            Permission.PRODUCT_REGISTER,
            product_created.id
        )


        return Result.success(None)



    def register_stock_entry(
        self,
        product_name: str,
        supplier_name: str,
        unit_price: Decimal,
        quantity: Decimal,
        expiration_date: datetime
    ) -> Result[None]:

        if self.get_user_role.lacks_permission(
            Permission.PRODUCT_REGISTER_STOCK_ENTRY
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para registrar entradas de stock."
            )


        try:
            stock_entry_created = StockEntry(
                product_name,
                supplier_name,
                unit_price,
                quantity,
                expiration_date
            )

        except DomainException as e:
            return Result.failure(str(e))


        try:
            product = self._product_repository.find_by_id(
                ProductName(product_name)
            )

        except DomainException:
            return Result.failure(
                "El producto no esta registrado."
            )


        if product is None:
            return Result.failure(
                "El producto no esta registrado."
            )

        print(product.get_stock().value)
        result = product.process_delivery_from_supplier(
            stock_entry_created.quantity.value
        )
        print(product.get_stock().value)

        if result.is_failure():
            return result
        print(product.get_stock().value)

        if not self._supplier_repository.exists_by_id(
            stock_entry_created.supplier_name
        ):
            return Result.failure(
                "El proveedor no esta registrado."
            )


        self._product_repository.save_stock_entry(
            stock_entry_created,
            product
        )


        self._register_user_action(
            Permission.PRODUCT_REGISTER_STOCK_ENTRY,
            stock_entry_created.id
        )


        return Result.success(None)



    # --------------------- READ ---------------------

    def find_product_by_id(
        self,
        product_id: str
    ) -> Optional[Product]:

        if self.get_user_role.lacks_permission(
            Permission.PRODUCT_FIND_BY_ID
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para buscar productos por ID."
            )


        try:
            product = self._product_repository.find_by_id(
                ProductName(product_id)
            )

            if product:
                self._register_user_action(
                    Permission.PRODUCT_FIND_BY_ID,
                    product.id
                )

            return product


        except DomainException:
            return None



    def find_product_by_bar_code(
        self,
        bar_code: str
    ) -> Optional[Product]:

        if self.get_user_role.lacks_permission(
            Permission.PRODUCT_FIND_BY_BAR_CODE
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para buscar productos por código de barras."
            )


        try:
            product = self._product_repository.find_by_bar_code(
                BarCode(bar_code)
            )


            if product:
                self._register_user_action(
                    Permission.PRODUCT_FIND_BY_BAR_CODE,
                    product.id
                )

            return product


        except DomainException:
            return None



    def find_all_products(
        self
    ) -> list[Product]:

        if self.get_user_role.lacks_permission(
            Permission.PRODUCT_FIND_ALL
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para buscar todos los productos."
            )


        products = self._product_repository.find_all_products()


        self._register_user_action(
            Permission.PRODUCT_FIND_ALL,
            AllId()
        )


        return products