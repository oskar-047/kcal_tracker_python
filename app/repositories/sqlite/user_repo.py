import sqlite3
from repositories.sqlite.helpers import fetch_last_inserted_row, get_row_by_id
from domain.user import UserData, UserWeight

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
            return None

        return UserData(**dict(user_data))



    def create_user(self, data: UserData) -> UserData:
        cursor = self.conn.execute(
            '''
            INSERT INTO user_data (
            name, height, is_male, kcal_target, activity_level, 
            protein_percent, carbs_percent, fats_percent, objective, lan
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (data.name, data.height, data.is_male, data.kcal_target,
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
            """
            UPDATE user_data
            SET
            name=COALESCE(?, name),
            age=COALESCE(?, age),
            height=COALESCE(?, height),
            is_male=COALESCE(?, is_male),
            kcal_target=COALESCE(?, kcal_target),
            activity_level=COALESCE(?, activity_level),
            protein_percent=COALESCE(?, protein_percent),
            carbs_percent=COALESCE(?, carbs_percent),
            fats_percent=COALESCE(?, fats_percent),
            objective=COALESCE(?, objective),
            lan=COALESCE(?, lan)
            WHERE id=?
            """,
            (data.name, data.age, data.height, data.is_male, data.kcal_target,
            data.activity_level, data.protein_percent, data.carbs_percent,
            data.fats_percent, data.objective, data.lan, data.id),
        )
        self.conn.commit()
        return get_row_by_id(self.conn, "user_data", data.id, UserData)



    def get_user_lan(self, user_id: int) -> str | None:
        lan = self.conn.execute(
            '''
            SELECT lan 
            FROM user_data
            WHERE id=?
            ''',
            (user_id,)
        ).fetchone()

        return lan[0] if lan else "en"

    def change_user_lan(self, user_id, lan) -> bool:
        cursor = self.conn.execute(
            '''
            UPDATE user_data 
            SET lan=?
            WHERE id=?
            ''',
            (lan, user_id))

        return True if cursor.rowcount > 0 else False

    def track_weight(self, user_id: int, weight: float) -> float:
        cur = self.conn.execute(
            "INSERT INTO user_weight(user_id, weight) VALUES(?, ?)",
            (user_id, weight),
        )

        row_id = cur.lastrowid

        return self.conn.execute(
            "SELECT weight FROM user_weight WHERE id=?",
            (row_id,),
        ).fetchone()[0]

    def get_all_tracked_weights(self, user_id) -> list[UserWeight] | None:
        rows = self.conn.execute(
            '''
            SELECT user_id, weight, tracked_date 
            FROM user_weight
            WHERE user_id=?
            ''',
            (user_id,)
        ).fetchall()

        if not rows:
            return None

        return [UserWeight(**dict(row)) for row in rows]
