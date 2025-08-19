import sqlite3
from db.database import DB_PATH

def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def create_default_user(lan: str, return_user: bool):
    with _get_conn() as conn:
        row = conn.execute("SELECT * FROM user_data LIMIT 1").fetchone()
        if not row:
            conn.execute(
            '''
            INSERT INTO user_data (lan) VALUES(?)
            ''', (lan,))
        conn.commit()

        if return_user:
            return conn.execute("SELECT * FROM user_data LIMIT 1").fetchone()

        return None

def get_user_from_db(conn, id):

    row = conn.execute(
        '''
        SELECT * FROM user_data WHERE id=?
        ''',
        (id,)
    ).fetchone()
    
    return dict(row) if row else None

def fetch_last_inserted_row(conn, table: str, id: int, model_cls):
    row = conn.execute(
        f'''
        SELECT * FROM {table}
        WHERE id=?
        ''',
        (id,)
    ).fetchone()

    if not row:
        raise RuntimeError(f"Inserted {table} row not found")

    return model_cls(**dict(row))


def get_row_by_id(conn, table: str, id: int, model_cls):
    row = conn.execute(
        f'''
        SELECT * FROM {table}
        WHERE id=?
        ''',
        (id,)
    ).fetchone()

    if not row:
        raise RuntimeError(f"{table} row with id {id} not found")

    return model_cls(**dict(row))