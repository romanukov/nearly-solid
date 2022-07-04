import os

from ns.deps.startup import setup
from ns.entities import EntityABC
from ns.settings.base.abc import SettingsABC
from ns.settings.fields import config

SQLITE_URL = 'sqlite:///dev.db'
os.environ.setdefault('DB_URL', SQLITE_URL)


class Settings(SettingsABC):
    DB_URL: str = config()
    PERSON_COUNT: int = config(default=10)


class User(EntityABC):
    __id__ = 'username'

    username: str
    password: str
    full_name: str
    active: bool


class GoodUser(User):
    good: bool
    bad_user: 'BadUser'


class BadUser(User):
    bad: bool
    good_user: 'GoodUser'


setup()


# db_engine = create_engine(Settings.DB_URL)
# meta = MetaData()
# DBSession = sessionmaker(bind=db_engine)
# TablesBuilder(db_engine).generate_entities_tables([GoodUser.__details__, BadUser.__details__], True)
