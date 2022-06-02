
class BaseDataMeta(type):
    """
    Базовый метакласс для метаклассов данных
    """
    base_cls_name: str

    @classmethod
    def build_cls(mcs, cls: type): ...

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if cls.__name__ != mcs.base_cls_name:
            mcs.build_cls(cls)
        return cls


class BaseEntityMeta(BaseDataMeta):
    """
    Базовый метакласс для сущностей
    """


class BaseValueMeta(BaseDataMeta):
    """
    Базовый метакласс для значений
    """
