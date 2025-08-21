from contextlib import contextmanager
from db.database import get_db

@contextmanager
def db_conn():
    gen = get_db()
    conn = next(gen)           # open
    try:
        yield conn             # let caller use it
        next(gen, None)        # commit + close
    except Exception:
        try:
            gen.throw(Exception("rollback"))  # trigger rollback
        except StopIteration:
            pass
        raise
