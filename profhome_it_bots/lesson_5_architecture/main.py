from argparse import ArgumentParser

import uvicorn
from fastapi import FastAPI

from src import setup_application
from src.utils import read_config


if __name__ == '__main__':
    parser = ArgumentParser(description='Bot CLI arguments')

    DEFAULT_CONFIG_PATH = './app_config.yaml'

    parser.add_argument('-c', '--config', help='Path to the app configuration file', type=str, required=False, default=DEFAULT_CONFIG_PATH)
    parser.add_argument('-s', '--server_config', help='Path to the server configuration file', type=str, required=False, default=None)
    args = parser.parse_args()

    app: FastAPI = setup_application(args)

    config = {}
    if args.server_config:
        config = read_config(args.server_config)

    uvicorn.run(app, **config)
