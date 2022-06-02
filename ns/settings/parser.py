from abc import ABC
from os import environ

from ns.settings.errors import SettingsError, SettingsErrorCodes


class ISettingsParser(ABC):
    def get_setting(self, key: str, cast: type = str): ...


class EnvSettingsParser(ISettingsParser):
    def get_setting(self, key: str, cast: type = str):
        if key not in environ:
            raise SettingsError(SettingsErrorCodes.SETTING_KEY_IS_REQUIRED, key=key)
        try:
            value = cast(environ[key])
        except ValueError as err:
            raise SettingsError(SettingsErrorCodes.INVALID_VALUE_FOR_CAST, message=str(err))
        return value
