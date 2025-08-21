import sqlite3
from repositories.sqlite.helpers import fetch_last_inserted_row, get_row_by_id
from domain.food import Meal

class SQLiteMealRepo:
    def __init__(self, conn):
        self.conn = conn

    def list_meals(self, start: int, end: int) -> list[Meal]:
        rows = self.conn.execute(
            '''
            SELECT id, food_id, quantity, tracked_date, meal_type
            FROM meals
            WHERE tracked_date BETWEEN ? AND ?;
            ''',
            (start, end)
            ).fetchall()


        return [Meal(**dict(row)) for row in rows]


    def create_meal(self, meal: Meal) -> Meal:
        cursor = self.conn.execute(
            '''
            INSERT INTO meals (food_id, quantity, tracked_date, meal_type)
            VALUES (?, ?, ?, ?)
            ''',
            (meal.food_id, meal.quantity, meal.tracked_date, meal.meal_type)
        )

        last_id = cursor.lastrowid
        
        return fetch_last_inserted_row(self.conn, "meals", last_id, Meal)


    def delete_meal(self, id: int) -> bool:
        cursor = self.conn.execute(
            '''
            DELETE FROM meals
            WHERE id=?
            ''',
            (id,)
        )

        return cursor.rowcount > 0



    def edit_meal(self, meal: Meal) -> Meal | None:
        self.conn.execute(
            '''
            UPDATE meals
            SET food_id=?, quantity=?, tracked_date=?, meal_type=?
            WHERE id=?
            ''',
            (meal.food_id, meal.quantity, meal.tracked_date, meal.meal_type, meal.id)
        )

        self.conn.commit()

        return get_row_by_id(self.conn, "meals", meal.id, Meal)

