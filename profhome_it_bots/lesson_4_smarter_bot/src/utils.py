import json
import os
from pathlib import Path

import yaml


def read_config(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        if Path(path).suffix[1:] == "yaml":
            return yaml.safe_load(f)
        return json.load(f)


def get_token(token: str | None) -> str:
    env_token = os.getenv('API_TOKEN')

    if token is None and env_token is None:
        raise ValueError('The HTTP API token must be provided via the API_TOKEN environment variable or the -t command-line argument!')

    token = env_token if env_token else token

    if len(token) == 0:
        raise ValueError('The HTTP API token must be a non-empty string')

    return token
