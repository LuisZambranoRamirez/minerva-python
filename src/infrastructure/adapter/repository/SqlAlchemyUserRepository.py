from domain.constants.Role import Role
from typing import Optional

from sqlalchemy.orm import Session

from domain.entities.user.User import User as DomainUser
from domain.entities.user.UserId import UserId
from domain.entities.userAction.UserAction import UserAction as DomainUserAction

from domain.repositories.UserRepository import UserRepository

from domain.valueObject.DNI import DNI

from infrastructure.persistence.models import (
    User as UserModel,
    Useraction as UserActionModel
)


class SqlAlchemyUserRepository(UserRepository):

    def __init__(
        self,
        session: Session
    ):
        self.session = session


    def save(
        self,
        user: DomainUser
    ) -> None:

        model = UserModel(
            username=user.username.value,
            dni=user.dni.value,
            names=user.names.value,
            lastnames=user.last_names.value,
            password=user.password_hash.value,
            rolename=user.role,
            isactive=user.is_active,
            registrationdate=user.registration_date
        )

        self.session.merge(model)
        self.session.commit()



    def save_user_action(
        self,
        user_action: DomainUserAction
    ) -> None:

        model = UserActionModel(
            useractionid=str(
                user_action.user_action_id
            ),
            username=user_action.user_name.value,
            permission=user_action.permission,
            entityid=str(
                user_action.entity_id
            ),
            registrationdate=user_action.registration_date
        )

        self.session.add(model)
        self.session.commit()



    def exists_by_id(
        self,
        id: UserId
    ) -> bool:

        return (
            self.session.query(UserModel)
            .filter(
                UserModel.username == id.get_value()
            )
            .first()
            is not None
        )



    def exists_by_dni(
        self,
        dni: DNI
    ) -> bool:

        return (
            self.session.query(UserModel)
            .filter(
                UserModel.dni == dni.value
            )
            .first()
            is not None
        )



    def find_by_id(
        self,
        id: UserId
    ) -> Optional[DomainUser]:

        model = (
            self.session.query(UserModel)
            .filter(
                UserModel.username == id.get_value()
            )
            .first()
        )

        if model is None:
            return None

        return self._to_domain(model)



    def _to_domain(
        self,
        model: UserModel
    ) -> DomainUser:

        return DomainUser.restore(
            dni=model.dni,
            names=model.names,
            last_names=model.lastnames,
            username=model.username,
            password_hash=model.password,
            role=Role(model.rolename),
            is_active=model.isactive,
            registration_date=model.registrationdate
        )