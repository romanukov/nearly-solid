from ns.commands.abc import CommandsABC

from application.shop.entities import Product
from application.shop.repo import IProductsRepo, IOrdersRepo


class AdminCommands(CommandsABC):
    products_repo: IProductsRepo
    orders_repo: IOrdersRepo

    def create_product(self, **kwargs) -> Product:
        return self.products_repo.create(**kwargs)

    def update_product(self, **kwargs) -> Product: ...

    def delete_product(self, name: str): ...

    def create_order(self, **kwargs) -> Product: ...

    def update_order(self, **kwargs) -> Product: ...

    def delete_order(self, order_id: int): ...
