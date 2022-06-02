from dataclasses import dataclass


@dataclass
class ConfigField:
    key: str = ''
    required: bool = True
    cast: type = None


def config(key: str = '', required: bool = True, cast: type = str):
    return ConfigField(key=key, required=required, cast=cast)
