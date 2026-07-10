from domain.interfaces.PasswordHasher import PasswordHasher

from domain.valueObject.Password import Password
from domain.valueObject.PasswordHash import PasswordHash


import bcrypt


class BcryptPasswordHasher(PasswordHasher):


    def hash(
        self,
        raw_password: Password
    ) -> PasswordHash:

        password_bytes = (
            raw_password.value
            .encode("utf-8")
        )

        salt = bcrypt.gensalt()

        hashed = bcrypt.hashpw(
            password_bytes,
            salt
        )

        return PasswordHash(
            hashed.decode("utf-8")
        )



    def matches(
        self,
        password: str,
        hashed_password: PasswordHash
    ) -> bool:

        password_bytes = (
            password.encode("utf-8")
        )

        hashed_bytes = (
            hashed_password.value
            .encode("utf-8")
        )

        return bcrypt.checkpw(
            password_bytes,
            hashed_bytes
        )