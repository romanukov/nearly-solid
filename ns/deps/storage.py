"""
Глобальное хранилище всех зависимостей
"""
from ns.deps.interface import IContainer
from ns.deps.structs import Register

COMPONENTS: Register = Register()
ENTITIES: Register = Register()
VALUES: Register = Register()

CONTAINERS: dict[str, IContainer] = {}
CONTAINER: Register = Register()
DEPENDENCIES: Register = Register()
