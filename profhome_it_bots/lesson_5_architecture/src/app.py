from argparse import Namespace

from fastapi import FastAPI

from .databases import setup_databases
from .routes import register_routes
from .utils import read_config


def setup_application(args: Namespace) -> FastAPI:

    app = FastAPI(title='FastAPI application template', description='My first FastAPI application!')

    config = read_config(args.config)

    setup_databases(app, config.get('databases', {}))
    register_routes(app, config.get('routes', {}))

    return app
