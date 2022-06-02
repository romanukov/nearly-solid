from ns.settings.build import SettingsBuilder


class SettingsMeta(type):
    """
    Запуск сборки настроек
    """
    builder: SettingsBuilder = SettingsBuilder()

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if cls.__name__ != 'SettingsABC':
            mcs.builder.build(cls)
            cls = cls()
        return cls
