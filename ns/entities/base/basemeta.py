from abc import abstractmethod

from ns.deps import storage
from ns.entities.errors import EntitiesError, ErrorCodes


class BaseDataMeta(type):
    """
    Базовый метакласс для метаклассов данных
    """
    base_cls_name: str

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        # Сборка должна выполняться во всех классах кроме базового
        if cls.__name__ != mcs.base_cls_name:
            mcs.register_cls(cls)
        return cls

    @classmethod
    def register_cls(mcs, cls: type):
        """
        Регистрирует класс в регистре типов
        """
        if mcs.base_cls_name == 'EntityABC':
            storage.ENTITIES.set(cls.__name__, cls)
        elif mcs.base_cls_name == 'ValueABC':
            storage.VALUES.set(cls.__name__, cls)
        else:
            raise EntitiesError(
                ErrorCodes.DATA_CLASS_WAS_NOT_REGISTERED,
                base_cls=mcs.base_cls_name,
                cls_name=cls.__name__,
            )


class BaseEntityMeta(BaseDataMeta):
    """
    Базовый метакласс для сущностей
    """


class BaseValueMeta(BaseDataMeta):
    """
    Базовый метакласс для значений
    """
