from abc import ABC

from domain.repositories.UserRepository import UserRepository
from domain.constants.Permission import Permission
from domain.constants.Role import Role
from domain.entities.userAction.UserAction import UserAction
from domain.exceptions.DomainException import DomainException
from domain.interfaces.Id import Id
from domain.valueObject.id.UserName import UserName


class Service(ABC):

    def __init__(
        self,
        user_role: Role,
        user_name: UserName,
        user_repository: UserRepository,
    ):
        if user_role is None:
            raise RuntimeError(
                "El usuario debe tener un rol, no puede ser nulo."
            )

        if user_name is None:
            raise RuntimeError(
                "El nombre del usuario no puede ser nulo."
            )

        self._user_role = user_role
        self._user_name = user_name
        self._user_repository = user_repository

    # Como segunda barrera de defensa aquí también podría validarse
    # que el rol tenga permiso para ejecutar la acción.
    def _register_user_action(
        self,
        permission: Permission,
        entity_id: Id,
    ) -> None:

        try:
            self._user_repository.save_user_action(
                UserAction(
                    self._user_name,
                    permission,
                    entity_id,
                )
            )

        except DomainException as e:
            raise RuntimeError(str(e)) from e

    @property
    def get_user_role(self) -> Role:
        return self._user_role