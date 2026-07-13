from domain.constants.Role import Role
from infrastructure.api.Oauth2 import create_access_token
from infrastructure.api.dependencies import get_user_service
from application.services.UserService import UserService
from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from pydantic import BaseModel


from infrastructure.api.dependencies import CurrentUser, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


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

@router.get("/me")
def get_me(
    current_user: CurrentUser = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    user = service._user_repository.find_by_id(current_user.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return {
        "username": user.username.value,
        "dni": user.dni.value,
        "names": user.names.value,
        "last_names": user.last_names.value,
        "role": user.role.value
    }

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

