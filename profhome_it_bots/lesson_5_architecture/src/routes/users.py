from typing import Annotated

from fastapi import Depends, FastAPI, status
from sqlalchemy import false, select

from .auth import authenticate_user
from ..databases import PostgreSQLManager
from ..databases.postgresql.user import User as DBUser
from ..schemas import User


def register_users_endpoints(app: FastAPI):

    @app.get('/users', status_code=status.HTTP_200_OK, tags=['Users'])
    async def register(user: Annotated[User, Depends(authenticate_user)]) -> list[User]:
        """
        Endpoint that returns all registered common (non-admin) users.
        """

        db = PostgreSQLManager().database
        users = await db.fetch_all(select(DBUser).where(DBUser.is_admin == false()))

        return list(map(User.model_validate, users))
