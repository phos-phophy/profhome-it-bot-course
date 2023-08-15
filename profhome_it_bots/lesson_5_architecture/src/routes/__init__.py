from fastapi import FastAPI

from .auth import register_auth_endpoints


def register_routes(app: FastAPI, config: dict):
    register_auth_endpoints(app)
