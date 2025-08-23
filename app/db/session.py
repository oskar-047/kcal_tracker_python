from contextlib import contextmanager
from db.database import get_db

@contextmanager
def db_conn():
    gen = get_db()          # start dependency generator
    conn = next(gen)        # yields the connection
    try:
        yield conn          # let caller use it
    except BaseException as exc:
        # propagate the REAL exception into get_db() so it can rollback
        try:
            gen.throw(exc)
        except StopIteration:
            pass
        raise               # re-raise original
    else:
        # normal path → commit/close inside get_db()
        try:
            next(gen)
        except StopIteration:
            pass
