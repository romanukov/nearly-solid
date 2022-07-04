from application.shop.commands import ShopCommands
from ns.deps.startup import setup
from ns.deps.utils import resolve_depend
from ns.deps.finder import Finder



setup()

commands_instance: ShopCommands = resolve_depend(ShopCommands)

from application.shop.entities import Product
print(commands_instance.products_repo)
