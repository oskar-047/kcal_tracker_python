import sqlite3
from pathlib import Path

DB_PATH = (Path(__file__).resolve().parent / "app_database.db")

def get_db():

    conn = sqlite3.connect(DB_PATH)

    # This is how sqlite returns the data, per default it returns a tuple that must be accesed by index, with sqlite3.row it returns a object similar to a dictionary where you can acces by column name
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")

    # Returns the conn and when its used automatically closes the connection
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise # re-throws the error to FastAPI
    finally:
        conn.close()