from ns.entities import EntityABC


class User(EntityABC):
    __id__ = 'email'

    email: str
    password: str
