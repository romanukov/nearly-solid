from adapters.repo import UsersRepo
from application.admin.repo import IUsersRepo
from application.admin.commands import AdminCommands
from application.admin.queries import AdminQueries
from ns.deps.container import Container


class AdminContainer(Container):
    users_repo: IUsersRepo = UsersRepo()
    commands: AdminCommands = AdminCommands()
    queries: AdminQueries = AdminQueries()
