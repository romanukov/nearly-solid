
from ns.deps.component import Component, ComponentMeta


class CommandsMeta(ComponentMeta):
    ...


class CommandsABC(Component, metaclass=CommandsMeta):
    """
    Базовый класс для команд бизнес-логики. Все не приватные и не магические
    методы этого класса будут зарегистрированы как команды.

    Команда - неидемпонетнтая операция (функция) бизнес-логики.
    """
