from application.admin.repo import IUsersRepo
from application.shop.repo import IProductsRepo, IOrdersRepo
from ns.database.repos.interfaces import T


class ProductsRepo(IProductsRepo):

    def create(self, **data: any) -> T:
        print('create')

    def list(self, limit: int, offset: int) -> list[T]:
        print('list')

    def one(self, entity_id: any) -> T:
        print('one')

    def update(self, entity_id: any, **data: any) -> T:
        print('update')

    def delete(self, entity_id: any):
        print('delete')


class OrdersRepo(IOrdersRepo):

    def create(self, **data: any) -> T:
        print('create')

    def list(self, limit: int, offset: int) -> list[T]:
        print('list')

    def one(self, entity_id: any) -> T:
        print('one')

    def update(self, entity_id: any, **data: any) -> T:
        print('update')

    def delete(self, entity_id: any):
        print('delete')


class UsersRepo(IUsersRepo):

    def create(self, **data: any) -> T:
        print('create')

    def list(self, limit: int, offset: int) -> list[T]:
        print('list')

    def one(self, entity_id: any) -> T:
        print('one')

    def update(self, entity_id: any, **data: any) -> T:
        print('update')

    def delete(self, entity_id: any):
        print('delete')