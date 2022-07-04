from ns.queries.abc import QueriesABC

from application.shop.entities import Product, Order
from application.shop.repo import IProductsRepo, IOrdersRepo


class AdminQueries(QueriesABC):
    products_repo: IProductsRepo
    orders_repo: IOrdersRepo

    def get_products(self, limit: int, offset: int) -> list[Product]: ...

    def get_product(self, name: str) -> Product: ...

    def get_orders(self, limit: int, offset: int) -> list[Order]: ...

    def get_order(self, order_id: int) -> Order: ...
