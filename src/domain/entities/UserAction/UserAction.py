from datetime import datetime

from domain.constants.Permission import Permission
from domain.entities.userAction.UserActionId import UserActionId
from domain.exceptions.DomainException import DomainException
from domain.exceptions.UnexpectedDomainException import UnexpectedDomainException
from domain.interfaces.Entity import Entity
from domain.interfaces.Id import Id
from domain.valueObject.id.UserActionIdImpl import UserActionIdImpl
from domain.valueObject.id.UserName import UserName


class UserAction(Entity[UserActionId]):

    def __init__(
        self,
        user_name: UserName,
        permission: Permission,
        entity_id: Id,
    ):
        temp_id = UserActionIdImpl.generate()

        super().__init__(temp_id)

        self._user_action_id = temp_id
        self._user_name = user_name

        if permission is None:
            raise DomainException(
                "El permiso no puede ser nulo."
            )

        self._permission = permission

        if entity_id is None:
            raise DomainException(
                "El ID de la entidad no puede ser nulo."
            )

        self._entity_id = entity_id
        self._registration_date = datetime.now()

    @classmethod
    def restore(
        cls,
        user_action_id: str,
        user_name: UserName,
        permission: Permission,
        entity_id: Id,
        registration_date: datetime,
    ) -> "UserAction":

        try:
            user_action = cls.__new__(cls)

            temp_id = UserActionIdImpl.from_string(
                user_action_id
            )

            Entity.__init__(user_action, temp_id)

            user_action._user_action_id = temp_id
            user_action._user_name = user_name
            user_action._permission = permission
            user_action._entity_id = entity_id
            user_action._registration_date = registration_date

            return user_action

        except DomainException as e:
            raise UnexpectedDomainException(
                f"Error al crear la acción de usuario: {str(e)}",
                e,
            )

    # -------------------------------------

    @property
    def user_action_id(self) -> UserActionIdImpl:
        return self._user_action_id

    @property
    def user_name(self) -> UserName:
        return self._user_name

    @property
    def permission(self) -> Permission:
        return self._permission

    @property
    def entity_id(self) -> Id:
        return self._entity_id

    @property
    def registration_date(self) -> datetime:
        return self._registration_date