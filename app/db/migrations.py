import sqlite3

def column_exists(conn, table: str, col: str) -> bool:
    # The query returns a tuple with info for each column on the table, accessing the position 1 to 
    # read the column name, if some column on the table matches the col parameter it means the table 
    # contains that column
    return any(result[1] == col for result in conn.execute(f"PRAGMA table_info({table})"))

def table_exists(conn, table: str) -> bool:
    result = conn.execute(
        '''
        SELECT 1 
        FROM sqlite_master
        WHERE type='table'
        AND name=?
        ''',
        (table,)
    ).fetchone()

    return result is not None

def index_exists(conn, index: str) -> bool:
    result = conn.execute(
        '''
        SELECT 1
        FROM sqlite_master
        WHERE type='index'
        AND name=?
        ''',
        (index,)
    ).fetchone()

    return result is not None


def migration_1(conn):
    if not column_exists(conn, "user_data", "objective"):
        conn.execute("ALTER TABLE user_data ADD COLUMN objective INTEGER DEFAULT (0)")

def migration_2(conn):
    if not column_exists(conn, "user_food", "is_deleted"):
        conn.execute("ALTER TABLE user_food ADD COLUMN is_deleted INTEGER DEFAULT (0)")