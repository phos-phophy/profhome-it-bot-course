from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..schemas import User, JWTToken
from ..database import add_user, get_user


AUTH_URL = '/user/auth'


def register_auth_endpoints(app: FastAPI):

    exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"WWW-Authenticate": "Bearer"}
    )

    @app.post('/user/register', status_code=status.HTTP_201_CREATED)
    async def register(data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> User:
        """
        Endpoint that registers new common (non-admin) user and return its schema.
        """

        user_in_db: User | None = await get_user(data.username)

        if user_in_db:
            exception.detail = 'This username is already occupied!'
            raise exception

        new_user = User.new_user(data, 'common')
        await add_user(new_user)

        return new_user

    @app.post(AUTH_URL, status_code=status.HTTP_200_OK, response_model=JWTToken)
    async def auth(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        """
        Endpoint that authenticates user and returns its JWT token.
        """

        user_in_db: User | None = await get_user(data.username)

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

    user = await get_user(data[0], data[1])

    if not user:
        raise exception

    return user
