import sqlite3
from repositories.sqlite.helpers import fetch_last_inserted_row, get_row_by_id
from domain.user import UserData

class SQLiteUserRepo():
    def __init__(self, conn):
        self.conn = conn

    def get_user(self, user_id: int) -> UserData:
        user_data = self.conn.execute(
            '''
            SELECT * FROM user_data
            WHERE id=?
            ''',
            (user_id,)
        ).fetchone()

        if not user_data:
            raise RuntimeError("User not found")

        return UserData(**dict(user_data))



    def create_user(self, data: UserData) -> UserData:
        cursor = self.conn.execute(
            '''
            INSERT INTO user_data (
            name, height, birthdate, is_male, activity_level,
            protein_percent, carbs_percent, fats_percent, objective, lan
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (data.name, data.height, data.birthdate, data.is_male,
            data.activity_level, data.protein_percent, data.carbs_percent,
            data.fats_percent, data.objective, data.lan)
        )

        last_id = cursor.lastrowid
        return fetch_last_inserted_row(self.conn, "user_data", last_id, UserData)

    def create_user_minimal(self, lan: str) -> UserData:
        cur = self.conn.execute(
            "INSERT INTO user_data(lan) VALUES (?)", (lan,)
        )
        return get_row_by_id(self.conn, "user_data", 1, UserData)


    def edit_user(self, data: UserData) -> UserData:
        self.conn.execute(
            '''
            UPDATE user_data
            SET name=?, height=?, birthdate=?, is_male=?, activity_level=?,
            protein_percent=?, carbs_percent=?, fats_percent=?, objective=?, lan=?
            WHERE id=?
            ''',
            (data.name, data.height, data.birthdate, data.is_male,
            data.activity_level, data.protein_percent, data.carbs_percent,
            data.fats_percent, data.objective, data.lan, data.id)
        )

        return get_row_by_id(self.conn, "user_data", data.id, UserData)


    def get_user_lan(self, user_id: int) -> str | None:
        lan = self.conn.execute(
            '''
            SELECT lan 
            FROM user_data
            WHERE id=?
            ''',
            (user_id,)
        ).fetchone()[0]

        return lan if lan else None

    def change_user_lan(self, user_id, lan) -> bool:
        cursor = self.conn.execute(
            '''
            UPDATE user_data 
            SET lan=?
            WHERE id=?
            ''',
            (lan, user_id))

        return True if cursor.rowcount > 0 else False


