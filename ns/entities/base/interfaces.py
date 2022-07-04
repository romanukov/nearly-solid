from typing import TypeVar

from ns.entities.details import EntityDetails, ValueDetails


class IEntityMagic:
    """
    Интерфейс магии сущностей
    """
    __id__: str
    __details__: EntityDetails
    __relations__: EntityDetails


class IValueMagic:
    """
    Интерфейс магии значений
    """
    __natural_key__: list[str]
    __details__: ValueDetails


EntityType = TypeVar('EntityType')
ValueType = TypeVar('ValueType')
