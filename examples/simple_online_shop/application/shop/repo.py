from abc import ABC

from ns.database.repos.interfaces import ICRUDRepo

from application.shop.entities import Product, Order


class IProductsRepo(ICRUDRepo[Product]):
    ...


class IOrdersRepo(ICRUDRepo[Order]):
    ...
