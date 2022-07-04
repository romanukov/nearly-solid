from inspect import getmembers

from ns.deps import storage


class ComponentMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name != 'Component':
            storage.COMPONENTS.set(name, cls)
            members = dict(getmembers(cls))
            if '__annotations__' in members:
                annotations: dict[str, type] = members['__annotations__']
                dependencies = []
                for field_name, t in annotations.items():
                    if isinstance(t, ComponentMeta):
                        dependencies.append((field_name, t))
                storage.DEPENDENCIES.set(name, dependencies)
        return cls


class Component(metaclass=ComponentMeta):
    ...

