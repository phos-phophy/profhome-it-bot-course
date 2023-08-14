from argparse import Namespace


from fastapi import FastAPI

from .routes import register_routes


def setup_application(args: Namespace) -> FastAPI:

    app = FastAPI(title='FastAPI application template', description='My first FastAPI application!')

    register_routes(app)

    return app
