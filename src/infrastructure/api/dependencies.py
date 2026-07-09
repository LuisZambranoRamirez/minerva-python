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