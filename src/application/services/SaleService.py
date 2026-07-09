from domain.entities.product.ProductId import ProductId
from domain.entities.sale.DTO import SaleItem
from domain.entities.sale.DTO import PayData

from application.services.Service import Service
from typing import Optional

from domain.constants.Permission import Permission
from domain.constants.Role import Role
from domain.entities.product.Product import Product
from domain.entities.result.Result import Result
from domain.repositories.ProductRepository import ProductRepository
from domain.valueObject.ProductQuantity import ProductQuantity
from domain.valueObject.id.AllId import AllId
from domain.valueObject.id.CustomerName import CustomerName
from domain.entities.sale.Sale import Sale
from domain.exceptions.DomainException import DomainException
from domain.exceptions.UnauthorizedActionException import UnauthorizedActionException
from domain.repositories.SaleRepository import SaleRepository
from domain.repositories.UserRepository import UserRepository
from domain.valueObject.id.SaleIdImpl import SaleIdImpl
from domain.valueObject.id.UserName import UserName
from domain.repositories.CustomerRepository import CustomerRepository



class SaleService(Service):

    def __init__(
        self,
        user_role: Role,
        user_name: UserName,
        user_repository: UserRepository,
        sale_repository: SaleRepository,
        customer_repository: CustomerRepository,
        product_repository: ProductRepository
    ):
        super().__init__(
            user_role,
            user_name,
            user_repository
        )

        self._sale_repository = sale_repository
        self._customer_repository = customer_repository
        self._product_repository = product_repository


    # --------------------- WRITE ---------------------

    def register_sale(
        self,
        customer_id: str,
        pays: list[PayData],
        items: list[SaleItem]
    ) -> Result:

        if self.get_user_role.lacks_permission(
            Permission.SALE_REGISTER
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para registrar ventas."
            )

        try:
            sale_created = Sale(
                customer_id,
                items
            )

            if self._customer_repository.find_by_id(
                CustomerName(customer_id)
            ) is None:
                return Result.failure(
                    "Cliente no encontrado."
                )

            add_pays_result = sale_created.add_pays(pays)

            if add_pays_result.is_failure():
                return add_pays_result


            product_quantities: dict[
                ProductId,
                ProductQuantity
            ] = sale_created.get_product_quantities()


            products: set[Product] = (
                self._product_repository.find_all_by_ids(
                    set(product_quantities.keys())
                )
            )


            if len(products) != len(product_quantities):
                return Result.failure(
                    "Uno o más productos no encontrados."
                )


            for product in products:
                product.process_sale(
                    product_quantities[
                        product.id
                    ].value
                )


            self._sale_repository.save(
                sale_created,
                products
            )


            self._register_user_action(
                Permission.SALE_REGISTER,
                sale_created.id
            )

            return Result.success(None)


        except DomainException as e:
            return Result.failure(
                str(e)
            )


    def add_payment_to_sale(
        self,
        sale_id_str: str,
        pays: list[PayData]
    ) -> Result:

        if self.get_user_role.lacks_permission(
            Permission.SALE_ADD_PAYMENT
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para agregar pagos a ventas."
            )


        try:
            sale_id_impl = SaleIdImpl.from_string(
                sale_id_str
            )

        except DomainException as e:
            return Result.failure(
                str(e)
            )


        sale = self._sale_repository.find_by_id(
            sale_id_impl
        )


        if sale is None:
            return Result.failure(
                "Venta no encontrada."
            )


        add_payment_result = sale.add_pays(
            pays
        )


        if add_payment_result.is_failure():
            return add_payment_result


        self._sale_repository.update_payments(
            sale
        )


        self._register_user_action(
            Permission.SALE_ADD_PAYMENT,
            sale.id
        )


        return Result.success(None)


    # --------------------- READ ---------------------


    def find_sale_by_id(
        self,
        sale_id: str
    ) -> Optional[Sale]:

        if self.get_user_role.lacks_permission(
            Permission.SALE_FIND_BY_ID
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para buscar ventas por ID."
            )


        try:
            sale = self._sale_repository.find_by_id(
                SaleIdImpl.from_string(sale_id)
            )


            if sale is not None:

                self._register_user_action(
                    Permission.SALE_FIND_BY_ID,
                    sale.id
                )

            return sale


        except DomainException:
            return None



    def find_sales_by_customer_id(
        self,
        customer_id: str
    ) -> list[Sale]:

        if self.get_user_role.lacks_permission(
            Permission.SALE_FIND_BY_CUSTOMER_ID
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para buscar ventas por ID de cliente."
            )


        try:
            sales = self._sale_repository.find_by_customer_id(
                CustomerName(customer_id)
            )


            for sale in sales:
                self._register_user_action(
                    Permission.SALE_FIND_BY_CUSTOMER_ID,
                    sale.id
                )


            return sales


        except DomainException:
            return []



    def find_all_sales(self) -> list[Sale]:

        if self.get_user_role.lacks_permission(
            Permission.SALE_FIND_ALL
        ):
            raise UnauthorizedActionException(
                "El usuario no tiene permiso para buscar todas las ventas."
            )


        sales = self._sale_repository.find_all()


        self._register_user_action(
            Permission.SALE_FIND_ALL,
            AllId()
        )


        return sales