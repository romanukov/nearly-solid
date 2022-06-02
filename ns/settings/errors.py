from enum import Enum


class SettingsErrorCodes(Enum):
    SETTING_KEY_IS_REQUIRED = 'SETTING_KEY_IS_REQUIRED'
    CONFIG_CANNOT_BE_PRIVATE = 'CONFIG_CANNOT_BE_PRIVATE'
    INVALID_VALUE_FOR_CAST = 'INVALID_VALUE_FOR_CAST'
    SETTING_TYPE_IS_NOT_ALLOWED = 'SETTING_TYPE_IS_NOT_ALLOWED'


class SettingsError(BaseException):
    def __init__(self, code: SettingsErrorCodes, **data: any):
        self.code = code
        self.data = data

    def __str__(self):
        result = []
        for name, value in self.__dict__.items():
            if name.startswith('_'):
                continue
            result.append(f'{name}={value}')
        result = ', '.join(result)
        return f'{self.__class__.__name__}({result})'

