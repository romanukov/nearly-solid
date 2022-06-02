from ns.entities.build.utils import is_entity, is_list_of_data, is_value
from ns.entities.details import Relation


class RelationBuilder:
    def build(self, cls: type, field_name: str, field_type: type) -> Relation:
        if cls_is_value := is_value(field_type) or is_entity(field_type):
            if hasattr(cls, field_name):
                raise ValueError(f'{cls.__name__}.{field_name} can not have a default value')
            return Relation(name=field_name, type=field_type, to_many=False, is_value=cls_is_value)
        if data_type := is_list_of_data(field_type):
            cls_is_value = is_value(data_type)
            return Relation(name=field_name, type=data_type, to_many=True, is_value=cls_is_value)
        raise ValueError(f'Relation for {cls.__name__}.{field_name} not created (field type: {field_type.__name__})')

    def is_relation(self, field_type: type) -> bool:
        return is_entity(field_type) or is_value(field_type) or is_list_of_data(field_type)
