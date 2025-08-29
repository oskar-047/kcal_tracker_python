import sqlite3
from repositories.sqlite.helpers import fetch_last_inserted_row, get_row_by_id
from domain.food import Food

class SQLiteFoodRepo:
    def __init__(self, conn):
        self.conn = conn

    def list_foods(self) -> list[Food]:
        rows = self.conn.execute(
            '''
            SELECT uf.name, uf.kcal, uf.protein, uf.carbs, uf.fats, uf.id, uf.food_id, uf.version_date
            FROM user_food AS uf
            JOIN (
                SELECT food_id, max(version_date) AS version_date
                FROM user_food
                GROUP BY food_id
            ) latest
            ON uf.food_id = latest.food_id AND uf.version_date = latest.version_date
            WHERE uf.is_deleted = 0
            '''
        ).fetchall()

        food_list: list[Food] = []

        for row in rows:
            dict_row = dict(row)

            food = Food(**dict_row)

            food_list.append(food)

        return food_list

    def create_food(self, food: Food) -> Food:
        cursor = self.conn.execute(
            '''
            
                INSERT INTO user_food (name, kcal, protein, carbs, fats)
                VALUES (?, ?, ?, ?, ?)
            
            ''',
            (food.name, food.kcal, food.protein, food.carbs, food.fats)
            )

        last_id = cursor.lastrowid
        
        self.conn.execute(
            '''
            UPDATE user_food
            SET food_id=?
            WHERE id=?
            ''',
            (last_id, last_id)
        )
        
        return fetch_last_inserted_row(self.conn, "user_food", last_id, Food)



    def delete_food(self, id: int) -> bool: 
        cursor = self.conn.execute(
            '''
            UPDATE user_food
            SET is_deleted = 1
            WHERE id=?
            ''',
            (id,)
        )

        return cursor.rowcount > 0



    def edit_food(self, food: Food) -> Food:

        cursor = self.conn.execute(
            '''
            
                INSERT INTO user_food (name, kcal, protein, carbs, fats, food_id, version_date)
                VALUES (?, ?, ?, ?, ?, ?, strftime('%s', 'now'))
            
            ''',
            (food.name, food.kcal, food.protein, food.carbs, food.fats, food.food_id)
        )

        last_id = cursor.lastrowid

        return fetch_last_inserted_row(self.conn, "user_food", last_id, Food)

    def get_food_by_id(self, food_id) -> Food | None:
        row = self.conn.execute(
            '''
            SELECT name, kcal, protein, carbs, fats, id, food_id
            FROM user_food
            WHERE id=?
            ''',
            (food_id,)
        ).fetchone()

        return Food(**dict(row)) if row else None