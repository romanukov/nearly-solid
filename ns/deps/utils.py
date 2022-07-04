from typing import Hashable

from ns.deps import storage
from ns.deps.errors import DependencyError, ErrorCodes


def register_depend(interface: Hashable, impl: any):
    storage.CONTAINER.set(interface, impl)


def resolve_depend(interface: Hashable) -> any:
    if interface not in storage.CONTAINER.data:
        raise DependencyError(ErrorCodes.DEPENDENCY_NOT_CONFIGURED, dependency=interface)
    return storage.CONTAINER.get(interface)
