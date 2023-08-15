import hashlib
import secrets

from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Extra


class User(BaseModel):
    """
    Schema that represents user. Can be sent to front.
    """

    username: str
    password: str
    is_admin: bool

    class Config:
        frozen = True
        extra = Extra.forbid
        from_attributes = True


class SaltedUser(User):
    """
    Schema that represents user with its salt. Don't send to front!.
    """

    salt: str

    @classmethod
    def new_user(cls, data: OAuth2PasswordRequestForm, is_admin: bool = False) -> 'SaltedUser':
        salt = secrets.token_urlsafe(20)
        return cls(
            username=data.username,
            password=_hash_password(data.password, salt),
            salt=salt,
            is_admin=is_admin
        )

    def check(self, data: OAuth2PasswordRequestForm) -> bool:
        return self.username == data.username and self.password == _hash_password(data.password, self.salt)


def _hash_password(password: str, salt: str, global_salt: str = '') -> str:
    """
    Utility function that hashes user password several times.
    """

    password = salt + password + global_salt

    for i in range(2**8):
        password = hashlib.sha512(password.encode()).hexdigest()

    return password
