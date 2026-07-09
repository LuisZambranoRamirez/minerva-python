from datetime import datetime

from domain.constants.Role import Role
from domain.entities.user.UserId import UserId
from domain.exceptions.DomainException import DomainException
from domain.exceptions.UnexpectedDomainException import UnexpectedDomainException
from domain.interfaces.Entity import Entity
from domain.interfaces.PasswordHasher import PasswordHasher
from domain.valueObject.DNI import DNI
from domain.valueObject.LastName import LastName
from domain.valueObject.Name import Name
from domain.valueObject.Password import Password
from domain.valueObject.PasswordHash import PasswordHash
from domain.valueObject.id.UserName import UserName


class User(Entity[UserId]):

    def __init__(
        self,
        password_hasher: PasswordHasher,
        dni: str,
        names: str,
        last_names: str,
        username: str,
        password: str,
        role: Role,
    ):
        temp_id = UserName(username)

        super().__init__(temp_id)

        self._dni = DNI(dni)
        self._names = Name(names)
        self._last_names = LastName(last_names)
        self._username = temp_id
        self._password_hash = password_hasher.hash(
            Password(password)
        )

        if role is None:
            raise DomainException(
                "El ROL no puede ser nulo."
            )

        self._role = role
        self._is_active = True
        self._registration_date = datetime.now()

    @classmethod
    def restore(
        cls,
        dni: str,
        names: str,
        last_names: str,
        username: str,
        password_hash: str,
        role: Role,
        is_active: bool,
        registration_date: datetime,
    ) -> "User":

        try:
            user = cls.__new__(cls)

            temp_id = UserName(username)

            Entity.__init__(user, temp_id)

            user._dni = DNI(dni)
            user._username = temp_id
            user._names = Name(names)
            user._last_names = LastName(last_names)
            user._password_hash = PasswordHash(
                password_hash
            )
            user._role = role
            user._is_active = is_active
            user._registration_date = registration_date

            return user

        except DomainException as e:
            raise UnexpectedDomainException(
                "Error al cargar el usuario",
                e,
            )

    # -------------------------------------

    @property
    def dni(self) -> DNI:
        return self._dni

    @property
    def names(self) -> Name:
        return self._names

    @property
    def last_names(self) -> LastName:
        return self._last_names

    @property
    def username(self) -> UserName:
        return self._username

    @property
    def password_hash(self) -> PasswordHash:
        return self._password_hash

    @property
    def role(self) -> Role:
        return self._role

    @property
    def is_active(self) -> bool:
        return self._is_active

    @property
    def registration_date(self) -> datetime:
        return self._registration_date