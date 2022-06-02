from inspect import getmembers, getdoc
from typing import Callable

from ns.entities.base.interfaces import ValueType
from ns.entities.build.field import FieldBuilder
from ns.entities.details import ValueDetails
from ns.entities.const import missing


class ValueBuilder:
    field_builder: FieldBuilder = FieldBuilder()

    def build(self, cls: ValueType):
        annotations: dict[str, type] = dict(getmembers(cls))['__annotations__']
        fields, relations = [], []
        for field_name, field_type in annotations.items():
            if field_name.startswith('_'):
                continue
            if self.field_builder.is_field(field_type):
                field = self.field_builder.build(cls, field_name, field_type)
                fields.append(field)
            else:
                raise ValueError(f'{cls.__name__}.{field_name}: type {field_type} is not allowed')
        natural_keys = self._get_natural_keys(cls)
        if not natural_keys:
            raise ValueError(f'{cls.__name__} have not natural keys')
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
                    raise ValueError(f'Field "{field.name}" is required for {_self.__class__.__name__}')

                if not isinstance(field_value, field.type):
                    raise ValueError(f'{_self.__class__.__name__}.{field.name} is not {field.type}. '
                                     f'Got {field_value}')
                setattr(_self, field.name, field_value)

        return init_method
