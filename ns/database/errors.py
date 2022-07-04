from enum import Enum

from ns.common.errors import Error


class ErrorCodes(Enum):
    FOREIGN_KEY_HAS_NO_BACK_REFERENCE = 'FOREIGN_KEY_HAS_NO_A_BACK_REFERENCE'


class DatabaseError(Error[ErrorCodes]):
    """
    Ошибки базы данных
    """
