from ns.deps import storage
from ns.deps.container import ContainerMeta
from ns.deps.finder import Finder
from ns.deps.utils import resolve_depend
from ns.entities.base.meta import ValueMeta, EntityMeta
from ns.entities.build.entity import EntityBuilder
from ns.entities.build.value import ValueBuilder

_after_register_datatypes = []


def setup():
    finder = Finder()
    contexts = finder.find_contexts()

    entities = finder.find_entities(contexts)
    values = finder.find_values(contexts)
    commands = finder.find_commands(contexts)
    queries = finder.find_queries(contexts)
    adapters_interfaces = finder.find_adapters_interfaces(contexts)
    adapters_impls = finder.find_adapters_impls(adapters_interfaces)

    containers = finder.find_containers()

    construct_datatypes(entities, values)
    inject_dependencies(containers)


def construct_datatypes(entities: dict[str, list[EntityMeta]], values: dict[str, list[ValueMeta]]):
    entity_builder = EntityBuilder()

    _entities = {}
    for context_name, context_entities in entities.items():
        for entity in context_entities:
            _entities[entity.__name__] = entity

    _values = {}
    for context_name, context_values in values.items():
        for value in context_values:
            _values[value.__name__] = value

    for entity_name, entities_classes in entities.items():
        for entity_cls in entities_classes:
            fields = []
            if hasattr(entity_cls, '__details__'):
                fields = entity_cls.__details__.fields
            entity_builder.build(_entities, _values, entity_cls, fields)

    value_builder = ValueBuilder()
    for value_name, values_classes in values.items():
        for value_cls in values_classes:
            fields = []
            if hasattr(value_cls, '__details__'):
                fields = value_cls.__details__.fields
            value_builder.build(_entities, _values, value_cls, fields)


def inject_dependencies(containers: dict[str, ContainerMeta]):
    for container_name, container in containers.items():
        container.register()
    for cls_name, deps in storage.DEPENDENCIES.data.items():
        cls_component = storage.COMPONENTS.get(cls_name)
        for field_name, dependency in deps:
            dependency_component = resolve_depend(dependency)
            setattr(cls_component, field_name, dependency_component)
