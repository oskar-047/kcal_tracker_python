import sqlite3
from repositories.sqlite.helpers import fetch_last_inserted_row, get_row_by_id
from domain.meal import Meal
from datetime import date
from collections import defaultdict

class SQLiteMealRepo:
    def __init__(self, conn):
        self.conn = conn

    def list_meals(self, start: int, end: int) -> list[Meal]:
        rows = self.conn.execute(
            '''
            SELECT id, food_id, quantity, tracked_date, meal_type, eaten
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


    def get_meal_eaten_status(self, meal_id) -> int:
        row = self.conn.execute(
            '''
            SELECT eaten
            FROM meals
            WHERE id=?
            ''',
            (meal_id,)
        ).fetchone()

        if row:
            return row["eaten"]
        else:
            raise ValueError(f"Meal {meal_id} not found")
            
    def set_meal_eaten_status(self, meal_id, eaten_status) -> bool:
        cursor = self.conn.execute(
            '''
            UPDATE meals
            SET eaten=?
            WHERE id=?
            ''',
            (eaten_status, meal_id)
        )

        return cursor.rowcount > 0

    # Function used in weights chart to get each day kcal
    def get_daily_kcal(self, min_dt: int, max_dt: int) -> defaultdict[date, int | None]:
        rows = self.conn.execute(
            '''
            SELECT DATE(m.tracked_date, 'unixepoch') AS dt,
            CAST(SUM(ROUND(m.quantity * f.kcal / 100, 0)) AS INTEGER) AS kcal
            FROM meals m
            JOIN user_food f ON m.food_id = f.id
            WHERE m.tracked_date >= ? AND m.tracked_date < ?
            GROUP BY dt
            ORDER BY dt
            ''',
            (min_dt, max_dt)
        ).fetchall()

        
        return defaultdict(lambda: None, {
            date.fromisoformat(row["dt"]): row["kcal"] for row in rows
        }) if rows else defaultdict(lambda: None) 

    def get_meals_by_foods(self, min_dt: int, max_dt: int, foods: list): #-> tuple[dict[int, str], dict[date, dict[int, dict[str, float]]]]:

        params = ",".join("?" for _ in foods)

        new_foods = foods[:]
        new_foods.append(min_dt)
        new_foods.append(max_dt)

        rows = self.conn.execute(
            f'''
            SELECT DATE(m.tracked_date, 'unixepoch') AS dt,
            SUM(m.quantity * f.kcal/100) AS kcal,
            SUM(m.quantity * f.protein/100) AS protein,
            SUM(m.quantity * f.carbs/100) AS carbs,
            SUM(m.quantity * f.fats/100) AS fats,
            SUM(m.quantity) AS q,
            MAX(f.name) AS name,
            f.id AS id,
            f.color AS color
            FROM meals m
            JOIN user_food f
            ON m.food_id = f.id
            WHERE m.food_id IN ({params})
            AND m.tracked_date >= ?
            AND m.tracked_date < ?
            GROUP BY dt, f.id
            ''',
            new_foods
        ).fetchall()

        result_foods = defaultdict(lambda: defaultdict(dict))
        food_names = defaultdict(lambda: None)

        for row in rows:
            result_foods[date.fromisoformat(row["dt"])][row["id"]] = {
                "quantity": row["q"],
                "kcal": row["kcal"],
                "protein": row["protein"],
                "carbs": row["carbs"],
                "fats": row["fats"],
            }

            food_names[row["id"]] = {"name": row["name"],"color": row["color"]}


        return food_names, result_foods
