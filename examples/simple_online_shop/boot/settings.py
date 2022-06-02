from ns.settings import SettingsABC, config


class Settings(SettingsABC):
    DATABASE_URL: str = config()

    DOMAIN: str = config()
    SECRET: str = config()
    ROOT_URL: str = config()
    HOST: str = config()
    PORT: int = config()
