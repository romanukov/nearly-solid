from enum import Enum

from ns.common.errors import Error


class ErrorCodes(Enum):
    SETTING_KEY_IS_REQUIRED = 'SETTING_KEY_IS_REQUIRED'
    CONFIG_CANNOT_BE_PRIVATE = 'CONFIG_CANNOT_BE_PRIVATE'
    INVALID_VALUE_FOR_CAST = 'INVALID_VALUE_FOR_CAST'
    SETTING_TYPE_IS_NOT_ALLOWED = 'SETTING_TYPE_IS_NOT_ALLOWED'


class SettingsError(Error[ErrorCodes]):
    """
    Ошибки загрузки настроек
    """
