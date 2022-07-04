from ns.database.repos.interfaces import ICRUDRepo

from application.admin.entities import User


class IUsersRepo(ICRUDRepo[User]):
    ...
