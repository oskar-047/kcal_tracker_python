import sqlite3
from pathlib import Path
from db.database import DB_PATH
from db.models import init_db
from db.migrations import migration_1, migration_2


# Current database version
LATEST_VERSION = 2

# Dictionary with migration functions
MIGRATIONS = {
    1: migration_1,
    2: migration_2
}

def run_migrations():
    try:

        # Gets the connectin
        conn = sqlite3.connect(DB_PATH)

        # Enforce the foreign key to avoid errors
        conn.execute("PRAGMA foreign_keys=ON")

        # Reads the current database version (from an internal int on the database)
        # Returns a tuple with a column with the int
        current_version = conn.execute("PRAGMA user_version").fetchone()[0]

        # In a fresh database user_version is always 0 so here to check if the tables are created we 
        # will check is user_version if 0, if it is, will call a function to create the tables and 
        # update the user_version to 1 or the corresponding version
        if current_version == 0 and is_fresh_db(conn):
            with conn:
                init_db(conn)
                conn.execute(F"PRAGMA user_version = {LATEST_VERSION}")
        else:
            for version in range(current_version + 1, LATEST_VERSION + 1):
                with conn:
                    MIGRATIONS[version](conn)
                    conn.execute(f"PRAGMA user_version = {version}")

    finally:
        conn.close()

def is_fresh_db(conn) -> bool:

    # Counts how many user tables are created on the db
    result = conn.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name not LIKE 'sqlite_%'"
    ).fetchone()[0]

    # this is like return true if n == 0
    return result == 0




# The reason to use the same conn in all migration functions and on init_db 
# its because in case something fails, the system can roll back all 
# the changes, if every function have its own conn and something fails, this can leave unfinished migrations.