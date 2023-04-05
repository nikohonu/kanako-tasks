import json
from pathlib import Path

import appdirs

conifg_path = Path(
    appdirs.user_config_dir(appname="kanako", appauthor="Niko Honu")
)
conifg_path.mkdir(exist_ok=True, parents=True)
config_file_path = conifg_path / "settings.json"


def _load():
    if config_file_path.exists():
        with config_file_path.open("r") as file:
            return json.load(file)
    else:
        return {}


def _save(data):
    with config_file_path.open("w") as file:
        json.dump(data, file)


def get(key):
    return _load().get(key, None)


def set(key, value):
    data = _load()
    data[key] = str(value)
    _save(data)
