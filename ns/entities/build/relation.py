from ns.entities.build.utils import is_entity, is_list_of_data, is_value
from ns.entities.details import Relation
from ns.entities.errors import EntitiesError, ErrorCodes


class RelationBuilder:
    def build(self, cls: type, field_name: str, field_type: type) -> Relation:
        if cls_is_value := is_value(field_type) or is_entity(field_type):
            if hasattr(cls, field_name):
                raise EntitiesError(ErrorCodes.FIELD_CAN_NOT_HAVE_DEFAULT_VALUE, field_name=field_name)
            return Relation(name=field_name, type=field_type, to_many=False, is_value=cls_is_value)
        if data_type := is_list_of_data(field_type):
            cls_is_value = is_value(data_type)
            return Relation(name=field_name, type=data_type, to_many=True, is_value=cls_is_value)
        raise EntitiesError(ErrorCodes.RELATION_WAS_NOT_CREATED, field_name=field_name, field_type=field_type)

    def is_relation(self, field_type: type) -> bool:
        return is_entity(field_type) or is_value(field_type) or is_list_of_data(field_type)
