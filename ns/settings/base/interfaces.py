from ns.settings.fields import ConfigField


class ISettingsMagic:
    """
    Интерфейс магии настроек
    """
    __settings_fields__: dict[str, ConfigField]
