from ns.settings.base.interfaces import ISettingsMagic
from ns.settings.build import SettingsBuilder


class SettingsBuildingMeta(type):
    """
    Запуск сборки настроек
    Делает класс настроек своим инстансом (СИНГЛТОН)
    """
    builder: SettingsBuilder = SettingsBuilder()

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        is_settings_magic = ISettingsMagic not in bases  # ISettingsMagic - интерфейс базового класса настроек
        if len(bases) and is_settings_magic:
            mcs.builder.build(cls)
            cls = cls()
        return cls
