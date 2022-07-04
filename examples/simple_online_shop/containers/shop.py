from adapters.repo import ProductsRepo, OrdersRepo
from application.shop.commands import ShopCommands
from application.shop.queries import ShopQueries
from application.shop.repo import IProductsRepo, IOrdersRepo
from ns.deps.container import Container


class ShopContainer(Container):
    products_repo: IProductsRepo = ProductsRepo()
    orders_repo: IOrdersRepo = OrdersRepo()
    commands: ShopCommands = ShopCommands()
    queries: ShopQueries = ShopQueries()
