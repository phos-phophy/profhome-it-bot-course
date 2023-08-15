from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import insert, select

from ..databases import PostgreSQLManager
from ..databases.postgresql.user import User as DBUser
from ..schemas import JWTToken, SaltedUser, User


AUTH_URL = '/user/auth'


def register_auth_endpoints(app: FastAPI):

    exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"}
    )

    @app.post('/user/register', status_code=status.HTTP_201_CREATED, tags=['Registration and authentication'])
    async def register(data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> User:
        """
        Endpoint that registers new common (non-admin) user and return its schema.
        """

        db = PostgreSQLManager().database
        user_in_db = await db.fetch_one(select(DBUser).where(DBUser.username == data.username))

        if user_in_db:
            exception.detail = 'This username is already occupied!'
            raise exception

        new_user = SaltedUser.new_user(data, is_admin=False)
        await db.execute(insert(DBUser), new_user.model_dump())

        return User.model_validate(new_user)

    @app.post(AUTH_URL, status_code=status.HTTP_200_OK, response_model=JWTToken, tags=['Registration and authentication'])
    async def auth(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        """
        Endpoint that authenticates user and returns its JWT token.
        """

        db = PostgreSQLManager().database
        user_in_db = await db.fetch_one(select(DBUser).where(DBUser.username == data.username))

        user_in_db = SaltedUser.model_validate(user_in_db) if user_in_db else user_in_db

        if not user_in_db or not user_in_db.check(data):
            exception.detail = 'Invalid credentials!'
            raise exception

        return JWTToken.generate_token(user_in_db, timedelta(hours=2))


oauth2 = OAuth2PasswordBearer(tokenUrl=AUTH_URL)


async def authenticate_user(token: Annotated[str, Depends(oauth2)]) -> User:
    """
    Utility function that authenticates user and can be used as a dependency injection.
    """

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials!",
        headers={"WWW-Authenticate": "Bearer"},
    )

    data = JWTToken.wrap_token(token).decode_token()

    if not data:
        raise exception

    db = PostgreSQLManager().database
    user = await db.fetch_one(select(DBUser).where(DBUser.username == data[0], DBUser.is_admin == data[1]))

    if not user:
        raise exception

    return User.model_validate(user)
