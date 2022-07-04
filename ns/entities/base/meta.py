from ns.entities.base.basemeta import BaseEntityMeta, BaseValueMeta


class EntityMeta(BaseEntityMeta):
    """
    Метакласс сущностей.
    """
    base_cls_name = 'EntityABC'


class ValueMeta(BaseValueMeta):
    """
    Метакласс обьектов-значений.
    """
    base_cls_name = 'ValueABC'
