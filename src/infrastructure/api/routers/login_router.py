from domain.constants.Role import Role
from infrastructure.api.Oauth2 import create_access_token
from infrastructure.api.dependencies import get_user_service
from application.services.UserService import UserService
from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from pydantic import BaseModel


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
    request: LoginRequest,
    service: UserService = Depends(get_user_service)
):
    result = service.authenticate(
        request.username,
        request.password
    )

    if result.is_failure():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result.get_message()
        )

    role = result.get_data()

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El rol del usuario no existe."
        )

    token = create_access_token(
        username=request.username,
        role=role.value
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/register")
def register(
    request: RegisterRequest,
    service: UserService = Depends(get_user_service)
):

    result = service.register(
        dni=request.dni,
        names=request.names,
        last_names=request.last_names,
        username=request.username,
        password=request.password,
        role=request.role
    )

    if result.is_failure():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get_message()
        )

    return {
        "message": "Usuario registrado correctamente."
    }


class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    dni: str
    names: str
    last_names: str
    username: str
    password: str
    role: Role
