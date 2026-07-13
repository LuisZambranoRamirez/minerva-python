from domain.constants.Role import Role
from domain.valueObject.id.UserName import UserName
from infrastructure.api.Oauth2 import oauth2_scheme
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from infrastructure.api.Oauth2 import decode_token
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

from typing import Generator
from sqlalchemy.orm import Session

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_customer_repository(db: Session = Depends(get_db)) -> CustomerRepository:
    return SqlAlchemyCustomerRepository(db)

def get_product_repository(db: Session = Depends(get_db)) -> ProductRepository:
    return SqlAlchemyProductRepository(db)

def get_sale_repository(
    product_repo: ProductRepository = Depends(get_product_repository),
    db: Session = Depends(get_db)
) -> SaleRepository:
    return SqlAlchemySaleRepository(product_repo, db)

def get_supplier_repository(db: Session = Depends(get_db)) -> SupplierRepository:
    return SqlAlchemySupplierRepository(db)

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return SqlAlchemyUserRepository(db)

def get_password_hasher() -> PasswordHasher:
    return BcryptPasswordHasher()

def get_user_service() -> UserService:
    return UserService(get_user_repository(), get_password_hasher())


class CurrentUser:
    def __init__(
        self,
        username: UserName,
        role: Role,
    ):
        self.username = username
        self.role = role

def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> CurrentUser:

    payload = decode_token(token)

    username = payload.get("sub")
    role = payload.get("role")

    if username is None or role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Información de usuario incompleta.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    return CurrentUser(
        username=UserName(username),
        role=Role(role),
    )


