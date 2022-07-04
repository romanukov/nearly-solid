from inspect import getmembers, getdoc
from typing import Callable

from ns.deps.errors import DependencyError
from ns.entities.base.interfaces import ValueType
from ns.entities.base.meta import EntityMeta, ValueMeta
from ns.entities.build.field import FieldBuilder
from ns.entities.details import ValueDetails, FieldDetails
from ns.entities.const import missing
from ns.entities.errors import EntitiesError, ErrorCodes


class ValueBuilder:
    field_builder: FieldBuilder = FieldBuilder()

    def build(self, entities: dict[str, EntityMeta], values: dict[str, ValueMeta], cls: ValueType, default_fields: list[FieldDetails] = []):
        annotations: dict[str, type] = dict(getmembers(cls))['__annotations__']
        fields, relations = [], []
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
            else:
                raise EntitiesError(ErrorCodes.TYPE_NOT_ALLOWED, field_name=field_name, field_type=field_type)
        natural_keys = self._get_natural_keys(cls)
        if not natural_keys:
            raise EntitiesError(ErrorCodes.VALUE_HAS_NO_NATURAL_KEY)
        if default_fields:
            fields.extend(default_fields)
        cls.__details__ = ValueDetails(
            name=cls.__name__,
            description=getdoc(cls),
            type=cls,
            fields=fields,
            natural_keys=natural_keys,
        )
        cls.__init__ = self._build_constructor(cls.__details__)

    def _get_natural_keys(self, cls: ValueType) -> list[str]:
        annotations: dict[str, type] = dict(getmembers(cls))['__annotations__']
        natural_keys = []
        if hasattr(cls, '__natural_key__'):
            natural_keys = cls.__natural_key__
        if not natural_keys:
            for field_name, field_type in annotations.items():
                natural_keys.append(field_name)
        return natural_keys

    def _build_constructor(self, details: ValueDetails) -> Callable:
        def init_method(_self, **kwargs):
            for field in details.fields:
                field_value = kwargs.get(field.name, field.default_value)
                if field_value is missing:
                    raise EntitiesError(ErrorCodes.FIELD_IS_REQUIRED, field_name=field.name)

                if not isinstance(field_value, field.type):
                    raise EntitiesError(ErrorCodes.TYPE_NOT_ALLOWED, field_name=field.name, field_type=field.type)
                setattr(_self, field.name, field_value)

        return init_method
