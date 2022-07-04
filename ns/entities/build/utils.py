from enum import EnumMeta
from typing import get_args, Optional, Union

from ns.entities.base.basemeta import BaseEntityMeta, BaseValueMeta
from ns.entities.const import PRIMITIVE_TYPES
from ns.entities.errors import EntitiesError, ErrorCodes


def is_primitive(field_type: type) -> bool:
    return field_type in PRIMITIVE_TYPES


def is_enum(field_type: type) -> bool:
    return isinstance(field_type, EnumMeta)


def is_entity(field_type: type) -> bool:
    return isinstance(field_type, BaseEntityMeta)


def is_value(field_type: type) -> bool:
    return isinstance(field_type, BaseValueMeta)


def is_list_of_data(field_type: Union[type, str]) -> Optional[type]:
    if isinstance(field_type, str) or field_type.__name__ != 'list':
        return
    generic_args_list = get_args(field_type)
    if len(generic_args_list) != 1:
        raise EntitiesError(ErrorCodes.LIST_MUST_HAVE_1_GENERIC_ARGUMENT)
    generic_arg: type = generic_args_list[0]
    if is_entity(generic_arg) or is_value(generic_arg):
        return generic_arg
    raise EntitiesError(ErrorCodes.LIST_MUST_HAVE_HAVE_ENTITY_ARGUMENT_IN_GENERIC)


def is_list_of(check_type: type, generic_type: type) -> bool:
    if check_type.__name__ != 'list':
        return False
    generic_args_list = get_args(check_type)
    if len(generic_args_list) != 1:
        return False
    generic_arg: type = generic_args_list[0]
    return isinstance(generic_arg, generic_type)
