from enum import Enum
from typing import TypeVar, Generic

T = TypeVar('T', bound=Enum)


class Error(BaseException, Generic[T]):
    code: T
    data: any

    def __init__(self, code: T, **data: any):
        self.code = code
        self.data = data

    def __str__(self):
        result = []
        for name, value in self.data.items():
            if name.startswith('_'):
                continue
            result.append(f'{name}={value}')
        result = ', '.join(result)
        return f'{self.__class__.__name__}({self.code.value})[{result}]'
