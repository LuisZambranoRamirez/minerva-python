from typing import Optional

from domain.constants.Role import Role
from domain.entities.result.Result import Result
from domain.entities.user.User import User
from domain.exceptions.DomainException import DomainException
from domain.interfaces.PasswordHasher import PasswordHasher
from domain.repositories.UserRepository import UserRepository
from domain.valueObject.id.UserName import UserName


class UserService:

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    # --------------------- WRITE ---------------------

    def register(
        self,
        dni: str,
        names: str,
        last_names: str,
        username: str,
        password: str,
        role: Role,
    ) -> Result[None]:

        try:
            user = User(
                self._password_hasher,
                dni,
                names,
                last_names,
                username,
                password,
                role,
            )

        except DomainException as e:
            return Result.failure(
                str(e)
            )

        if self._user_repository.exists_by_id(
            user.username
        ):
            return Result.failure(
                "Ya existe el usuario"
            )

        if self._user_repository.exists_by_dni(
            user.dni
        ):
            return Result.failure(
                "El DNI esta registrado con otro usuario"
            )

        self._user_repository.save(
            user
        )

        return Result.success(None)

    # --------------------- AUTH ---------------------

    def authenticate(
        self,
        username: str,
        password: str,
    ) -> Result[Role]:

        try:
            user_name = UserName(
                username
            )

        except DomainException as e:
            return Result.failure(
                str(e)
            )

        user: Optional[User] = (
            self._user_repository.find_by_id(
                user_name
            )
        )

        if user is None:
            return Result.failure(
                "Credenciales invalidas"
            )

        if not user.is_active:
            return Result.failure(
                "Credenciales invalidas"
            )

        if self._password_hasher.matches(
            password,
            user.password_hash,
        ):
            return Result.success(
                user.role
            )

        return Result.failure(
            "Credenciales invalidas"
        )