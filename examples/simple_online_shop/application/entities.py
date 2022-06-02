from ns.entities import EntityABC


class Product(EntityABC):
    name: str
    description: str
    quantity: int


class Order(EntityABC):
    id: int
    full_name: str
    phone: str
    products: list[Product]
