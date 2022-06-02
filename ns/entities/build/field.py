from ns.entities.build.utils import is_primitive, is_enum
from ns.entities.details import FieldDetails
from ns.entities.const import missing


class FieldBuilder:
    def build(self, cls: type, field_name: str, field_type: type) -> FieldDetails:
        default_value = getattr(cls, field_name) if hasattr(cls, field_name) else missing
        not_missing_or_none = default_value is not missing and default_value is not None
        if not_missing_or_none and not isinstance(default_value, field_type):
            raise ValueError(f'{cls.__name__}.{field_name} is not a {field_type}. Got: {default_value}')
        details = FieldDetails(name=field_name, type=field_type, default_value=default_value)
        setattr(cls, field_name, details)
        return details

    def is_field(self, field_type: type) -> bool:
        return is_primitive(field_type) or is_enum(field_type)
