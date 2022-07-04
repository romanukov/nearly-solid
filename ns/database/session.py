from contextvars import ContextVar

from sqlalchemy.orm import Session

db_session: ContextVar[Session] = ContextVar('db_session')
