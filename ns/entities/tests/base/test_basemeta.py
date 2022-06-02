from ns.entities.base.basemeta import BaseEntityMeta, BaseValueMeta


def test_entity_base_meta():
    assert isinstance(BaseEntityMeta, type)


def test_value_base_meta():
    assert isinstance(BaseValueMeta, type)
