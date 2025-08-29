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
    if not column_exists(conn, "user_food", "version_date"):
        conn.execute(
            '''
            ALTER TABLE user_food 
            ADD COLUMN version_date INTEGER DEFAULT NULL
            '''
        )

        conn.execute(
        '''
        UPDATE user_food 
        SET version_date = strftime('%s', 'now') 
        WHERE version_date IS NULL
        ''')

    if not column_exists(conn, "user_food", "food_id"):
        conn.execute(
            '''
            ALTER TABLE user_food
            ADD COLUMN food_id INTEGER DEFAULT NULL
            '''
        )

        conn.execute("UPDATE user_food SET food_id = id WHERE food_id IS NULL")


def migration_2(conn):
    if not column_exists(conn, "meals", "eaten"):
        conn.execute(
            '''
            ALTER TABLE meals
            ADD COLUMN eaten BOOLEAN DEFAULT 0
            '''
        )