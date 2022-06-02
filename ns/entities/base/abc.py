from ns.entities.base.interfaces import IEntityMagic, IValueMagic
from ns.entities.base.meta import EntityMeta, ValueMeta


class EntityABC(IEntityMagic, metaclass=EntityMeta):
    """
    Базовый класс сущности.
    """

    def __init__(self, **kwargs): ...

    def __str__(self):
        cls_name = self.__class__.__name__
        id_field_key = self.__details__.id_field_key
        self_id = getattr(self, id_field_key)
        return f'<{cls_name}({self.__details__.id_field_key}={self_id})>'

    def __repr__(self):
        fields = []
        for field in self.__details__.fields:
            field_value = getattr(self, field.name)
            fields.append(f'{field.name}={field_value.__repr__()}')
        for relation in self.__details__.relations:
            relation_value = getattr(self, relation.name)
            fields.append(f'{relation.name}={relation_value.__str__()}')
        fields = ', '.join(fields)
        return f'{self.__class__.__name__}({fields})'


class ValueABC(IValueMagic, metaclass=ValueMeta):
    """
    Базовый класс обьекта-значения.
    """

    def __init__(self, **kwargs): ...

    def __str__(self):
        return f'<{self.__repr__()}>'

    def __repr__(self):
        fields = []
        for field in self.__details__.fields:
            field_value = getattr(self, field.name)
            fields.append(f'{field.name}={field_value.__repr__()}')
        fields = ', '.join(fields)
        return f'{self.__class__.__name__}({fields})'
