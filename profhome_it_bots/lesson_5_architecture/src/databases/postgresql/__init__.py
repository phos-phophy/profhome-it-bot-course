import os

from databases import Database
from fastapi import FastAPI

from .manager import PostgreSQLManager


def setup_postgresql(app: FastAPI, config: dict) -> Database:
    database_url = os.getenv('POSTGRESQL_URL')
    database = Database(database_url, **config)

    db_manager = PostgreSQLManager()
    db_manager.database = database

    @app.on_event('startup')
    async def startup():
        await database.connect()

    @app.on_event('shutdown')
    async def shutdown():
        await database.disconnect()

    return database
