import sqlite3
from pathlib import Path
from db.database import DB_PATH

def init_db(conn):

    cursor = conn.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS user_data(
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        name            TEXT,
        age             INTEGER,
        height          INTEGER,
        is_male         BOOLEAN,
        kcal_target     INTEGER,
        activity_level  REAL,
        protein_percent REAL,
        carbs_percent   REAL,
        fats_percent    REAL,
        objective       INTEGER,
        lan             TEXT    DEFAULT 'en'
        )
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS user_weight(
        id              INTEGER     PRIMARY KEY AUTOINCREMENT,
        user_id         INTEGER     NOT NULL,
        weight          REAL        NOT NULL,
        tracked_date    INTEGER     DEFAULT (strftime('%s', 'now')),
        FOREIGN KEY (user_id)       REFERENCES user_data(id)
        )
        '''
    )


    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS user_food(
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        kcal        INTEGER NOT NULL,
        protein     REAL    NOT NULL,
        carbs       REAL    NOT NULL,
        fats        REAL    NOT NULL,
        is_deleted  BOOL    DEFAULT (0),
        version_date INTEGER DEFAULT (strftime('%s', 'now'),
        food_id     INTEGER DEFAULT NULL
        )
        '''
    )


    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS meals(
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        food_id         INTEGER NOT NULL,
        quantity        INTEGER NOT NULL,
        tracked_date    INTEGER DEFAULT (strftime('%s', 'now')),
        meal_type       INTEGER DEFAULT 0,
        eaten           BOOLEAN DEFAULT 0
        FOREIGN KEY     (food_id) REFERENCES user_food(id) ON DELETE CASCADE
        )
        '''
    )