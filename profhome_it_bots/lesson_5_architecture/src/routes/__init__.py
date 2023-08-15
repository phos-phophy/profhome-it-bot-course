from fastapi import FastAPI

from .auth import register_auth_endpoints
from .users import register_users_endpoints


def register_routes(app: FastAPI, config: dict):
    register_auth_endpoints(app)
    register_users_endpoints(app)
