from datetime import datetime, date, time
from domain.meal import Meal
from repositories.interfaces import MealRepo
from domain.food import Food
from repositories.interfaces import FoodRepo

def track_meal(meal_repo: MealRepo, food_id: int, quantity: int, dt: datetime):

    timestamp = int(dt.timestamp())

    meal = Meal(food_id=food_id, quantity=quantity, tracked_date=timestamp)

    return meal_repo.create_meal(meal)
    
def list_meals(meal_repo: MealRepo, food_repo: FoodRepo, dt: date|None=None) -> list[dict]:
    dt = dt or datetime.today()

    today_start_ts = datetime.combine(dt, time.min).timestamp()
    today_end_ts = datetime.combine(dt, time.max).timestamp()

    meals = meal_repo.list_meals(today_start_ts, today_end_ts)

    if len(meals) > 0:
        return meals_to_macros(meals, food_repo)

    return []


def meals_to_macros(meals: list[Meal], food_repo: FoodRepo) -> list[dict]:
    
    macros: list[dict] = []
    
    for meal in meals:
        food = food_repo.get_food_by_id(meal.food_id)

        if not food:
            continue
        
        multiplier = meal.quantity / 100

        macros.append({
            "name": food.name,
            "id": meal.id,
            "quantity": meal.quantity,
            "tracked_date": datetime.fromtimestamp(meal.tracked_date).date(),
            "kcal": round(food.kcal * multiplier, 0),
            "protein": round(food.protein * multiplier, 1),
            "carbs": round(food.carbs * multiplier, 1),
            "fats": round(food.fats * multiplier, 1),
        })

    return macros

def calculate_total_macros(meals: list[dict]) -> dict:
    totals = {"kcal": 0, "protein": 0, "carbs": 0, "fats": 0}
    for m in meals:
        totals["kcal"] += m["kcal"]
        totals["protein"] += m["protein"]
        totals["carbs"] += m["carbs"]
        totals["fats"] += m["fats"]
    return totals

def delete_meal(meal_repo: MealRepo, meal_id: int):

    return meal_repo.delete_meal(int(meal_id))
