"""Helps read .config file"""

import pydantic
from pathlib import Path


_CONFIG_FILEPATH = Path('.config').resolve()


class ConfigError(Exception):
    """Error raised whether an error happens reading config file"""


class Config(pydantic.BaseModel):
    access_token: str


def get_config(config_filepath: str = _CONFIG_FILEPATH) -> Config:
    """Reads config from .config file

    Attributes:
        config_filepath (str): the config file location. Defaults to
            _CONFIG_FILEPATH

    Returns:
        Config: a dataclass containing every pair key value defined in the
            config file.
    """
    pairs = {}
    try:
        with open(config_filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        clave, valor = line.split('=', 1)
                        pairs[clave.strip()] = valor.strip()
    except FileNotFoundError:
        raise ConfigError(f'File {config_filepath} does not exists')

    try:
        config = Config(access_token=pairs.get('access_token'))
    except pydantic.ValidationError as err:
        raise ConfigError(f'Impropery specified config file {err}')

    return config
