# infra/api/dependencies.py

from fastapi import Depends

from application.services.CustomerService import CustomerService


def get_customer_service() -> CustomerService:
    # Crear repositorios
    # Obtener usuario autenticado
    # Construir CustomerService

    return CustomerService(
        user_role=...,
        user_name=...,
        user_repository=...,
        customer_repository=...,
    )

def get_sale_service() -> SaleService:
    return SaleService(
        user_role=...,
        user_name=...,
        user_repository=...,
        sale_repository=...,
        customer_repository=...,
        product_repository=...,
    )

# infra/api/dependencies.py

def get_user_service() -> UserService:
    return UserService(
        user_repository=...,
        password_hasher=...,
    )