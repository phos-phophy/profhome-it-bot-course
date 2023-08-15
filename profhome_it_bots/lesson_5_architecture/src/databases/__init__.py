from fastapi import FastAPI

from .postgresql import PostgreSQLManager, setup_postgresql


def setup_databases(app: FastAPI, config: dict):
    setup_postgresql(app, config.get('postgresql', {}))


__all__ = [
    'PostgreSQLManager',
    'setup_databases'
]
