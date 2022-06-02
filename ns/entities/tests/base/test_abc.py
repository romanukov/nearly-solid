from ns.entities.base.abc import EntityABC, ValueABC
from ns.entities.base.interfaces import IEntityMagic, IValueMagic
from ns.entities.base.meta import EntityMeta, ValueMeta


def test_entity_inheritance():
    assert isinstance(EntityABC, EntityMeta)
    assert isinstance(EntityABC(), IEntityMagic)
    assert isinstance(EntityABC(), EntityABC)


def test_value_inheritance():
    assert isinstance(ValueABC, ValueMeta)
    assert isinstance(ValueABC(), IValueMagic)
    assert isinstance(ValueABC(), ValueABC)
