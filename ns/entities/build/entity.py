from inspect import getmembers, getdoc
from typing import Callable

from ns.entities.base.interfaces import EntityType
from ns.entities.build.utils import is_list_of
from ns.entities.build.field import FieldBuilder
from ns.entities.build.relation import RelationBuilder
from ns.entities.details import EntityDetails
from ns.entities.const import missing


class EntityBuilder:
    PK_DEFAULT_FIELD_NAMES = 'id', 'name'

    field_builder: FieldBuilder = FieldBuilder()
    relation_builder: RelationBuilder = RelationBuilder()

    def build(self, cls: EntityType):
        annotations: dict[str, type] = dict(getmembers(cls))['__annotations__']
        fields, relations = [], []
        id_field_name = self._get_id_field_name(cls)
        for field_name, field_type in annotations.items():
            if field_name.startswith('_'):
                continue
            if self.field_builder.is_field(field_type):
                field = self.field_builder.build(cls, field_name, field_type)
                fields.append(field)
            elif self.relation_builder.is_relation(field_type):
                relation = self.relation_builder.build(cls, field_name, field_type)
                relations.append(relation)
            else:
                raise ValueError(f'{cls.__name__}.{field_name}": type {field_type} is not allowed')
        cls.__details__ = EntityDetails(
            name=cls.__name__,
            description=getdoc(cls) if cls.__doc__ else '',
            type=cls,
            fields=fields,
            relations=relations,
            id_field_key=id_field_name,
        )
        cls.__init__ = self._build_constructor(cls.__details__)

    def _get_id_field_name(self, cls: EntityType) -> str:
        annotations: dict[str, type] = dict(getmembers(cls))['__annotations__']
        id_field_name = None
        if hasattr(cls, '__id__'):
            id_field_name = cls.__id__
        if not id_field_name:
            for field_name, field_type in annotations.items():
                if not id_field_name and field_name in self.PK_DEFAULT_FIELD_NAMES:
                    id_field_name = field_name
        if not id_field_name:
            raise ValueError(f'{cls.__name__} has no ID')
        return id_field_name

    def _build_constructor(self, details: EntityDetails) -> Callable:
        to_one_relations = details.to_one_relations
        to_many_relations = details.to_many_relations

        def init_method(_self, **kwargs):
            for field in details.fields:
                field_value = kwargs.get(field.name, field.default_value)
                if field_value is missing:
                    raise ValueError(f'Field {field.name} is required for {_self.__class__.__name__}')

                if not isinstance(field_value, field.type):
                    raise ValueError(f'{_self.__class__.__name__}.{field.name} is not {field.type}. '
                                     f'Got {field_value}')
                setattr(_self, field.name, field_value)

            for relation in to_one_relations:
                field_value = kwargs[relation.name] if relation.name in kwargs else None
                if field_value is not None and not isinstance(field_value, relation.type):
                    raise ValueError(f'{_self.__class__.__name__}.{relation.name} is not {relation.type}. '
                                     f'Got {field_value}')
                setattr(_self, relation.name, field_value)

            for relation in to_many_relations:
                field_value = kwargs[relation.name] if relation.name in kwargs else []
                if field_value and not is_list_of(field_value, relation.type):
                    raise ValueError(f'{_self.__class__.__name__}.{relation.name} is not list[{relation.type}]. '
                                     f'Got {field_value}')
                setattr(_self, relation.name, field_value)

        return init_method
