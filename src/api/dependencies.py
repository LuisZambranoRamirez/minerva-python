from application.services.ProductService import ProductService
from application.services.SupplierService import SupplierService
from application.services.CustomerService import CustomerService

from infrastructure.repositories.InMemoryProductRepository import InMemoryProductRepository
from infrastructure.repositories.InMemorySupplierRepository import InMemorySupplierRepository
from infrastructure.repositories.InMemoryCustomerRepository import InMemoryCustomerRepository


# Global in-memory repositories
product_repo = InMemoryProductRepository()
supplier_repo = InMemorySupplierRepository()
customer_repo = InMemoryCustomerRepository()

# Global services
product_service = ProductService(product_repo, supplier_repo)
supplier_service = SupplierService(supplier_repo)
customer_service = CustomerService(customer_repo)


def get_product_service() -> ProductService:
    return product_service


def get_supplier_service() -> SupplierService:
    return supplier_service


def get_customer_service() -> CustomerService:
    return customer_service
