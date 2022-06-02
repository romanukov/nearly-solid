from unittest.mock import MagicMock

from ns.entities.base.abc import EntityABC, ValueABC
from ns.entities.base.meta import EntityMeta, ValueMeta


def test_entity_cls_meta():
    assert type(EntityABC) == EntityMeta

    mock_builder = MagicMock()
    EntityMeta.entity_builder = mock_builder

    class TestClass(metaclass=EntityMeta):
        ...
    assert True


def test_value_cls_meta():
    assert type(ValueABC) == ValueMeta
