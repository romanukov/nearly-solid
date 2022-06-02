from ns.settings.base.abc import SettingsABC
from ns.settings.fields import config


class Settings(SettingsABC):
    DB_URL: str = config()
    PERSON_COUNT: int = config()


print(Settings)
