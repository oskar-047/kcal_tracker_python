import sqlite3
from db.database import DB_PATH

def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def create_default_user(lan):
    with _get_conn() as conn:
        row = conn.execute("SELECT * FROM user_data LIMIT 1").fetchone()
        if not row:
            conn.execute(
            '''
            INSERT INTO user_data (lan) VALUES(?)
            ''', (lan,))

def get_user_from_db(conn, id):

    row = conn.execute(
        '''
        SELECT * FROM user_data WHERE id=?
        ''',
        (id,)
    ).fetchone()
    
    return dict(row) if row else None