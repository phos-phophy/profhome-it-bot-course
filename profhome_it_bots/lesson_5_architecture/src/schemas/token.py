import os
from datetime import datetime, timedelta

from jose import JWTError, jwt
from pydantic import BaseModel, Extra

from .user import User


class JWTToken(BaseModel):
    """
    Schema that represents JWT token.
    """

    access_token: str
    token_type: str

    class Config:
        frozen = True
        extra = Extra.forbid
        from_attributes = True

    @classmethod
    def wrap_token(cls, token: str) -> 'JWTToken':
        """
        Wraps existing str token.
        """

        return cls(access_token=token, token_type='bearer')

    @classmethod
    def generate_token(cls, user: User, expires_delta: timedelta) -> 'JWTToken':
        """
        Generates JWT token for the given user.
        """

        data = {'sub': user.username, 'adm': user.is_admin, 'exp': datetime.utcnow() + expires_delta}
        return cls.wrap_token(jwt.encode(data, os.getenv('SECRET_KEY'), algorithm='HS256'))

    def decode_token(self) -> tuple[str, bool] | None:
        """
        Decodes JWT token and return user info.
        """

        try:
            payload = jwt.decode(self.access_token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        except JWTError:
            return None

        if not payload.get('sub') or not payload.get('adm') or not payload.get('exp') or payload.get('exp') < datetime.utcnow():
            return None

        return payload.get('sub'), payload.get('adm')
