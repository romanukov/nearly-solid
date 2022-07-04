from dataclasses import dataclass

from ns.entities.const import missing


@dataclass
class ConfigField:
    key: str = ''
    cast: type = None
    default: any = missing


def config(key: str = '', cast: type = str, default: any = missing):
    return ConfigField(key=key, cast=cast, default=default)
