from databases import Database

from ..utils import _Singleton


class PostgreSQLManager(metaclass=_Singleton):
    def __init__(self):
        self._database: Database | None = None

    @property
    def database(self) -> Database:
        if self._database is None:
            raise AttributeError("PostgreSQL database is not initialized")
        return self._database

    @database.setter
    def database(self, database: Database):
        if self._database is not None:
            raise AttributeError("PostgreSQL database already initialized")
        self._database = database
