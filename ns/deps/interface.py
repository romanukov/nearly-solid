from abc import abstractmethod


class IContainer:
    @classmethod
    @abstractmethod
    def register(cls): ...
