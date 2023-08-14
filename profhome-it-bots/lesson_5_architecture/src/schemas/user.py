import hashlib
from enum import Enum

from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Extra


class UserRole(str, Enum):
    common = 'common'
    admin = 'admin'


class User(BaseModel):
    """
    Schema that represents user.
    """

    username: str
    password: str
    role: UserRole

    class Config:
        frozen = True
        extra = Extra.forbid

    @classmethod
    def new_user(cls, data: OAuth2PasswordRequestForm, role: str) -> 'User':
        return cls(
            username=data.username,
            password=_hash_password(data.password),
            role=role.lower()
        )

    def check(self, data: OAuth2PasswordRequestForm) -> bool:
        return self.username == data.username and self.password == _hash_password(data.password)


def _hash_password(password: str, salt: str = '', global_salt: str = '') -> str:
    """
    Utility function that hashes user password several times.
    """

    password = salt + password + global_salt

    for i in range(2**8):
        password = hashlib.sha512(password.encode()).hexdigest()

    return password
