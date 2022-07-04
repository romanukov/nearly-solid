from inspect import getmembers, getdoc
from typing import Callable

from ns.deps.errors import DependencyError
from ns.entities.base.interfaces import EntityType
from ns.entities.base.meta import EntityMeta, ValueMeta
from ns.entities.build.field import FieldBuilder
from ns.entities.build.relation import RelationBuilder
from ns.entities.build.utils import is_list_of
from ns.entities.details import EntityDetails, FieldDetails
from ns.entities.const import missing
from ns.entities.errors import EntitiesError, ErrorCodes


class EntityBuilder:
    PK_DEFAULT_FIELD_NAMES = 'id', 'name'

    field_builder: FieldBuilder = FieldBuilder()
    relation_builder: RelationBuilder = RelationBuilder()

    def build(self, entities: dict[str, EntityMeta], values: dict[str, ValueMeta], cls: EntityType, default_fields: list[FieldDetails] = []):
        annotations: dict[str, type] = dict(getmembers(cls))['__annotations__']
        fields, relations = [], []
        id_field_name = self._get_id_field_name(cls)
        for field_name, field_type in annotations.items():
            if field_name.startswith('_'):
                continue
            if isinstance(field_type, str):
                try:
                    field_type = entities[field_type]
                except KeyError:
                    field_type = values[field_type]
            if self.field_builder.is_field(field_type):
                field = self.field_builder.build(cls, field_name, field_type)
                fields.append(field)
            elif self.relation_builder.is_relation(field_type):
                relation = self.relation_builder.build(cls, field_name, field_type)
                relations.append(relation)
            else:
                raise EntitiesError(ErrorCodes.TYPE_NOT_ALLOWED, field_name=field_name, field_type=field_type)
        if default_fields:
            fields.extend(default_fields)
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
            raise EntitiesError(ErrorCodes.ENTITY_HAS_NO_ID, entity=cls.__name__)
        return id_field_name

    def _build_constructor(self, details: EntityDetails) -> Callable:
        to_one_relations = details.to_one_relations
        to_many_relations = details.to_many_relations

        def init_method(_self, **kwargs):
            for field in details.fields:
                field_value = kwargs.get(field.name, field.default_value)
                if field_value is missing:
                    raise EntitiesError(ErrorCodes.FIELD_IS_REQUIRED, field_name=field.name)

                if not isinstance(field_value, field.type):
                    raise EntitiesError(ErrorCodes.INVALID_FIELD_TYPE, field_name=field.name, field_type=field.type)
                setattr(_self, field.name, field_value)

            for relation in to_one_relations:
                field_value = kwargs[relation.name] if relation.name in kwargs else None
                if field_value is not None and not isinstance(field_value, relation.type):
                    raise EntitiesError(ErrorCodes.INVALID_RELATION_TYPE, field_name=relation.name,
                                        field_type=relation.type)
                setattr(_self, relation.name, field_value)

            for relation in to_many_relations:
                field_value = kwargs[relation.name] if relation.name in kwargs else []
                if field_value and not is_list_of(field_value, relation.type):
                    raise EntitiesError(ErrorCodes.INVALID_RELATION_TYPE, field_name=relation.name,
                                        field_type=list[relation.type])
                setattr(_self, relation.name, field_value)

        return init_method
