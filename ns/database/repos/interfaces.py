from abc import abstractmethod, ABC
from typing import Generic, TypeVar, Callable

from ns.deps.component import Component
from ns.entities.base.meta import EntityMeta

T = TypeVar('T', bound=EntityMeta)


class IRepo(Component):
    ...


class ICRUDRepo(IRepo, Generic[T]):
    """
    Интерфейс репозитория, реализующий CRUD для сущности
    """

    def create(self, **data: any) -> T:
        """
        Создает сущность
        :param data: поля-данные сущности
        :return: Обьект сущности
        """

    def list(self, limit: int, offset: int) -> list[T]:
        """
        Отдает список сущностей
        :param limit: сколько сущностей показать
        :param offset: начиная с какой сущности в БД
        :return: Список сущностей
        """

    def one(self, entity_id: any) -> T:
        """
        Достает одну сущность по ее ID из хранилища и возвращает
        :param entity_id: ID сущности
        :return: объект сущности
        """

    def update(self, entity_id: any, **data: any) -> T:
        """
        Обновляет данные сущности в хранилище
        :param entity_id: ID сущности
        :param data: Данные сущности
        :return: Обьект сущности
        """

    def delete(self, entity_id: any):
        """
        Удаляет сущность в хранилище
        :param entity_id: ID сущности
        """
