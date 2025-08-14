import sqlite3
from pathlib import Path

DB_PATH = Path(app_database.db)

def init_db():

    # Gets a db connection
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS user_data(
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        name            TEXT    NOT NULL,
        height          INTEGER NOT NULL,
        birthdate       INTEGER NOT NULL,
        is_men          BOOLEAN,
        activity_level  REAL    DEFAULT (1.25),
        protein_percent REAL    DEFAULT (0.25),
        carbs_percent   REAL    DEFAULT (0.55),
        fats_percent    REAL    DEFAULT (0.2),
        objective       INTEGER DEFAULT (0)
        );


        CREATE TABLE IF NOT EXISTS user_weight(
        id              INTEGER     PRIMARY KEY AUTOINCREMENT,
        user_id         INTEGER     NOT NULL,
        weight          REAL        NOT NULL,
        tracked_date    INTEGER     DEFAULT (strftime('%s', 'now')),
        FOREIGN KEY (user_id)       REFERENCES user_data(id)
        );


        CREATE TABLE IF NOT EXISTS user_food(
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        kcal        INTEGER NOT NULL,
        protein     REAL    NOT NULL,
        carbs       REAL    NOT NULL,
        fats        REAL    NOT NULL
        );


        CREATE TABLE IF NOT EXISTS meal(
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        food_id         INTEGER NOT NULL,
        quantity        INTEGER NOT NULL,
        tracked_date    INTEGER DEFAULT (strftime('%s', 'now')),
        meal_type       INTEGER DEFAULT (0),
        FOREIGN KEY     (food_id) REFERENCES user_food(id) ON DELETE CASCADE
        )

        PRAGMA user_version = 1
        '''
    )