from ns.entities import EntityABC, ValueABC


class Product(EntityABC):
    name: str
    description: str
    quantity: int
    price: float


class Order(EntityABC):
    id: int
    email: str
    full_name: str
    phone: str
    address: 'Address'
    products: list[Product]


class Address(ValueABC):
    country: str
    state: str
    city: str
    street: str
    house: str
    flat: str = None
