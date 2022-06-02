from ns.settings.base.interfaces import ISettingsMagic
from ns.settings.base.meta import SettingsMeta


class SettingsABC(ISettingsMagic, metaclass=SettingsMeta):
    """
    Базовый класс синглтон-объекта настроек
    """

    def __str__(self):
        fields = []
        for key, field in self.__settings_fields__.items():
            value = getattr(self, key)
            fields.append(f'{key}={value.__repr__()}')
        fields = ', '.join(fields)
        return f'{self.__class__.__name__}({fields})'
