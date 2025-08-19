import sqlite3
from db.helpers import fetch_last_inserted_row, get_row_by_id
from app.domain.food import Food

class SQLiteFoodRepo:
    def __init__(self, conn):
        self.conn = conn

    def list_foods(self) -> list[Food]:
        rows = self.conn.execute(
            '''
            SELECT name, kcal, protein, carbs, fats, id 
            FROM user_food
            WHERE is_deleted=0
            ''').fetchall()

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
        self.conn.execute(
            '''
            UPDATE user_food
            SET name=?, kcal=?, protein=?, carbs=?, fats=?
            WHERE id=?
            ''',
            (food.name, food.kcal, food.protein, food.carbs, food.fats, food.id,)
        )

        self.conn.commit()

        return get_row_by_id(self.conn, "user_food", food.id, Food)