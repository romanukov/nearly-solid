from abc import ABC
from os import environ

from ns.entities.const import missing
from ns.settings.errors import SettingsError, ErrorCodes


class ISettingsParser(ABC):
    def get_setting(self, key: str, cast: type = str, default: any = missing): ...


class EnvSettingsParser(ISettingsParser):
    def get_setting(self, key: str, cast: type = str, default: any = missing):
        if key not in environ:
            if default is missing:
                raise SettingsError(ErrorCodes.SETTING_KEY_IS_REQUIRED, key=key)
            value = default
        else:
            value = environ[key]
        try:
            value = cast(value)
        except ValueError as err:
            raise SettingsError(ErrorCodes.INVALID_VALUE_FOR_CAST, message=str(err))
        return value
