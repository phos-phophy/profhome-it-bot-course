import json
from pathlib import Path

import yaml


def read_config(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        if Path(path).suffix[1:] == "yaml":
            return yaml.safe_load(f)
        return json.load(f)
