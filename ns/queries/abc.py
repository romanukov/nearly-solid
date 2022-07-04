from ns.deps.component import Component, ComponentMeta


class QueriesMeta(ComponentMeta):
    ...


class QueriesABC(Component, metaclass=QueriesMeta):
    """
    Базовый класс для запросов бизнес-логики. Все не приватные и не магические
    методы этого класса будут зарегистрированы как запросы.

    Запрос - идемпонетнтая операция (функция) бизнес-логики.
    Обычно какой-то геттер данных.
    """
