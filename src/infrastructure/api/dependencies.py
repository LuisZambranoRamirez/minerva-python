from application.services.UserService import UserService
from domain.interfaces.PasswordHasher import PasswordHasher
from infrastructure.adapter.repository.SqlAlchemyProductRepository import SqlAlchemyProductRepository
from infrastructure.adapter.repository.SqlAlchemySaleRepository import SqlAlchemySaleRepository
from infrastructure.adapter.repository.SqlAlchemySupplierRepository import SqlAlchemySupplierRepository
from domain.repositories.SupplierRepository import SupplierRepository
from domain.repositories.SaleRepository import SaleRepository
from domain.repositories.ProductRepository import ProductRepository
from domain.repositories.CustomerRepository import CustomerRepository
from domain.repositories.UserRepository import UserRepository
from infrastructure.adapter.BcryptPasswordHasher import BcryptPasswordHasher
from infrastructure.adapter.repository.SqlAlchemyUserRepository import SqlAlchemyUserRepository
from infrastructure.persistence.session import SessionLocal
from infrastructure.adapter.repository.SqlAlchemyCustomerRepository import SqlAlchemyCustomerRepository

def get_customer_repository() -> CustomerRepository:
    return SqlAlchemyCustomerRepository(SessionLocal())

def get_product_repository() -> ProductRepository:
    return SqlAlchemyProductRepository(SessionLocal())

def get_sale_repository() -> SaleRepository:
    return SqlAlchemySaleRepository(SessionLocal())

def get_supplier_repository() -> SupplierRepository:
    return SqlAlchemySupplierRepository(SessionLocal())

def get_user_repository() -> UserRepository:
    return SqlAlchemyUserRepository(SessionLocal())

def get_password_hasher() -> PasswordHasher:
    return BcryptPasswordHasher()

def get_user_service() -> UserService:
    return UserService(get_user_repository(), get_password_hasher())