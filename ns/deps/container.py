from abc import abstractmethod
from inspect import getmembers
from typing import Hashable

from ns.deps import storage
from ns.deps.errors import DependencyError, ErrorCodes
from ns.deps.interface import IContainer
from ns.deps.utils import register_depend


class ContainerMeta(type):
    __dependencies__: dict[Hashable, any] = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name != 'Container':
            cls.__dependencies__ = mcs._parse_dependencies(cls)
        return cls

    @classmethod
    def _parse_dependencies(mcs, cls: type) -> dict[Hashable, any]:
        result = {}
        annotations: dict[str, type] = dict(getmembers(cls))['__annotations__']
        for annotation_name, annotation_type in annotations.items():
            if not hasattr(cls, annotation_name):
                raise DependencyError(ErrorCodes.CONTAINER_FIELD_NOT_HAVE_VALUE, field=annotation_name)
            result[annotation_type] = getattr(cls, annotation_name)
        return result

    @abstractmethod
    def register(cls): ...


class Container(IContainer, metaclass=ContainerMeta):
    @classmethod
    def register(cls):
        print('resolving')
        for dep_cls, dep_impl in cls.__dependencies__.items():
            register_depend(dep_cls, dep_impl)

