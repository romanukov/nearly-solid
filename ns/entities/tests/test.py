from enum import Enum

from ns.entities import EntityABC, ValueABC


class Address(ValueABC):
    country: str
    zip: str
    city: str
    state: str
    street: str
    house: str

    def kek(self) -> tuple:
        print('kek')


class SomeEnum(Enum):
    SOME = 'SOME'
    ENUM = 'ENUM'
    KEK = 'KEK'


class SomeClass(EntityABC):
    """
    Some class
    """
    id: int
    a: str = None
    some: SomeEnum
    b: int = 123

    def kek(self) -> tuple:
        print('kek')


class SomeClass1(EntityABC):
    """
    Some class 1
    """
    name: str
    some_int: int
    some_cls: SomeClass
    some_cls1: list[SomeClass]
    some_address: Address

    def kek(self) -> tuple:
        print('kek')


t = SomeClass1(
    name='asd',
    some_int=123,
    some_cls=SomeClass(
        id=123,
        a='qwe',
        some=SomeEnum.SOME,
    ),
    some_address=Address(
        country='kek',
        zip='kek',
        city='kek',
        state='kek',
        street='kek',
        house='kek',
    ),
)
print(Address.__details__)
