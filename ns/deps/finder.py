import importlib
from os import getcwd, listdir, environ
from os.path import join, isdir
from typing import Type

from ns.commands.abc import CommandsMeta, CommandsABC
from ns.deps.component import ComponentMeta, Component
from ns.deps.container import ContainerMeta, Container
from ns.deps.errors import DependencyError, ErrorCodes
from ns.entities import EntityABC, ValueABC
from ns.entities.base.meta import EntityMeta, ValueMeta
from ns.queries.abc import QueriesMeta, QueriesABC


Impls = tuple[ComponentMeta, list[Type[ComponentMeta]]]  # Тип списка реализаций выбранного интерфейса


class Finder:
    environ.setdefault('PROJECT_PATH', getcwd())
    environ.setdefault('APPLICATION_MODULE_NAME', 'application')
    environ.setdefault('ADAPTERS_MODULE_NAME', 'adapters')
    environ.setdefault('CONTAINERS_MODULE_NAME', 'containers')

    @property
    def PROJECT_PATH(self) -> str:
        return environ['PROJECT_PATH']

    @property
    def APPLICATION_MODULE_NAME(self) -> str:
        return environ['APPLICATION_MODULE_NAME']

    @property
    def ADAPTERS_MODULE_NAME(self) -> str:
        return environ['ADAPTERS_MODULE_NAME']

    @property
    def CONTAINERS_MODULE_NAME(self) -> str:
        return environ['CONTAINERS_MODULE_NAME']

    @property
    def application_layer_path(self):
        return join(self.PROJECT_PATH, self.APPLICATION_MODULE_NAME)

    @property
    def containers_path(self):
        return join(self.PROJECT_PATH, self.CONTAINERS_MODULE_NAME)

    def find_contexts(self) -> list[str]:
        """
        Находит все контексты и отдает список их названий
        Контекстом считается пакет в модуле со слоем приложения
        Названием контекста считается имя такого пакета
        """
        contexts = []
        for file_name in listdir(self.application_layer_path):
            file_path = join(self.application_layer_path, file_name)
            if not file_name.startswith('_') and file_name != 'common' and isdir(file_path):
                contexts.append(file_name)
        return contexts

    def find_entities(self, contexts: list[str]) -> dict[str, list[EntityMeta]]:
        """
        Находит все сущности для каждого контекста
        """
        entities = {}
        for context in contexts:
            module = self._get_context_module(context, 'entities')
            classes: list[EntityMeta] = self._get_classes_in_module(module, EntityMeta, EntityABC)
            entities[context] = classes
        return entities

    def find_values(self, contexts: list[str]) -> dict[str, list[ValueMeta]]:
        """
        Находит все объекты-значения для каждого контекста
        """
        values = {}
        for context in contexts:
            module = self._get_context_module(context, 'entities')
            classes: list[ValueMeta] = self._get_classes_in_module(module, ValueMeta, ValueABC)
            values[context] = classes
        return values

    def find_commands(self, contexts: list[str]) -> dict[str, list[CommandsMeta]]:
        """
        Находит все команды для каждого контекста
        """
        commands = {}
        for context in contexts:
            module = self._get_context_module(context, 'commands')
            classes: list[CommandsMeta] = self._get_classes_in_module(module, CommandsMeta, CommandsABC)
            commands[context] = classes
        return commands

    def find_queries(self, contexts: list[str]) -> dict[str, list[QueriesMeta]]:
        """
        Находит все запросы для каждого контекста
        """
        queries = {}
        for context in contexts:
            module = self._get_context_module(context, 'queries')
            classes: list[QueriesMeta] = self._get_classes_in_module(module, QueriesMeta, QueriesABC)
            queries[context] = classes
        return queries

    def find_adapters_interfaces(self, contexts: list[str]) -> dict[str, list[ComponentMeta]]:
        """
        Находит все интерфейсы адаптеров для каждого контекста
        """
        result = {}
        for context in contexts:
            module = self._get_context_module(context, 'repo')
            classes: list[ComponentMeta] = self._get_classes_in_module(module, ComponentMeta, Component)
            result[context] = []
            for cls in classes:
                modules_are_equals = cls.__module__ == module.__name__
                starts_with_i = cls.__name__.startswith('I')
                if modules_are_equals and starts_with_i:
                    result[context].append(cls)
                    print(cls)
        return result

    def find_adapters_impls(self, interfaces: dict[str, list[ComponentMeta]]) -> dict[str, list[Impls]]:
        """
        Среди всех пакетов в адаптере находит имплементации интерфейсов для каждого контекста
        Отдает словарь реализаций адаптеров
        """
        adapters_modules = self._get_all_adapters_modules()
        components: list[ComponentMeta] = []
        for module in adapters_modules:
            adapters_modules_components = self._get_classes_in_module(module, ComponentMeta, Component)
            components.extend(adapters_modules_components)
        impls: dict[str, list[Impls]] = {}
        for context_name, interfaces_classes in interfaces.items():
            impls[context_name] = []
            for interface in interfaces_classes:
                interface_impls = []
                for component in components:
                    if issubclass(component, interface) and component is not interface:
                        interface_impls.append(component)
                impls[context_name].append((interface, interface_impls))
        return impls


    def find_containers(self) -> dict[str, ContainerMeta]:
        """
        Находит все контейнеры в containers/*
        Именем контейнера будет считаться название файла без .py
        Предполагается, что 1 файл = 1 контейнер
        """
        containers = {}
        for file_name in listdir(self.containers_path):
            file_path = join(self.containers_path, file_name)
            if file_name.startswith('_') or not file_path.endswith('.py'):
                continue
            container_name = file_name.replace('.py', '')
            module = self._get_container_module(container_name)
            module_containers = self._get_classes_in_module(module, ContainerMeta, Container)
            if not module_containers:
                raise DependencyError(ErrorCodes.CONTAINER_NOT_FOUND_IN_CONTAINER_FILE)
            if len(module_containers) > 1:
                raise DependencyError(ErrorCodes.BETTER_THAN_1_CONTAINER_IN_FILE)
            containers[container_name] = module_containers[0]
        return containers

    def _get_context_module(self, context: str, module_name: str) -> any:
        module_name = f'{self.APPLICATION_MODULE_NAME}.{context}.{module_name}'
        return importlib.import_module(module_name)

    def _get_all_adapters_modules(self) -> list[any]:
        """
        https://stackoverflow.com/questions/3365740/how-to-import-all-submodules
        """

    def _get_container_module(self, module_name: str) -> any:
        module_name = f'{self.CONTAINERS_MODULE_NAME}.{module_name}'
        return importlib.import_module(module_name)

    def _get_classes_in_module(self, module: any, meta: type, base_class: type) -> list[any]:
        classes = []
        for name, value in module.__dict__.items():
            if isinstance(value, meta) and value is not base_class:
                classes.append(value)
        return classes
