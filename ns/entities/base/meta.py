from ns.entities.base.basemeta import BaseEntityMeta, BaseValueMeta
from ns.entities.build.entity import EntityBuilder
from ns.entities.build.value import ValueBuilder


class EntityMeta(BaseEntityMeta):
    """
    Запуск сборки сущностей.
    """
    base_cls_name = 'EntityABC'
    entity_builder = EntityBuilder()

    @classmethod
    def build_cls(mcs, cls: type):
        mcs.entity_builder.build(cls)


class ValueMeta(BaseValueMeta):
    """
    Запуск сборки обьектов-значений.
    """
    base_cls_name = 'ValueABC'
    value_builder = ValueBuilder()

    @classmethod
    def build_cls(mcs, cls: type):
        mcs.value_builder.build(cls)
