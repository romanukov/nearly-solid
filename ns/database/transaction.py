from functools import wraps

from ns.database.session import db_session


def transaction(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        session = db_session.get()
        try:
            result = fn(*args, **kwargs)
        except Exception:
            session.rollback()
            raise
        else:
            session.commit()
        finally:
            session.close()
        return result
    return wrapper
