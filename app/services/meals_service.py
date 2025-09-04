from datetime import datetime, date, time
from domain.meal import Meal
from repositories.interfaces import MealRepo
from repositories.interfaces import UserRepo
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
            "eaten": meal.eaten
        })

    return macros

def calculate_total_macros(user_repo: UserRepo, meals: list[dict]) -> dict:

    # Calculate how many macros have the user today
    totals = {"kcal": 0, "protein": 0, "carbs": 0, "fats": 0}
    for m in meals:
        totals["kcal"] += m["kcal"]
        totals["protein"] += m["protein"]
        totals["carbs"] += m["carbs"]
        totals["fats"] += m["fats"]

    # Round to 1 decimal
    totals = {k: round(v, 1) for k, v in totals.items()}

    # g means goals
    g = user_repo.get_user_goal(1)

    kcal_target = g["kcal_target"] + g["objective"]

    target = {
        "kcal": kcal_target,
        "protein": g["protein_percent"]/100*kcal_target/4,
        "carbs": g["carbs_percent"]/100*kcal_target/4,
        "fats": g["fats_percent"]/100*kcal_target/9
    }

    # function for making all macros dict with the data needed for the graphs
    def make_macro_dict(name: str, target):
        total = totals[name]
        return {
            "value": round(min(total, target)),
            "r_value": round(max(0, target-total)),
            "objective": round(target),
            "e_value": round(max(0, total-target)),
            "e_r_value": round(max(0, target*2-total))
        }

    today = {k: make_macro_dict(k, v) for k, v in target.items()}

    today["t"] = totals

    return today

def delete_meal(meal_repo: MealRepo, meal_id: int):

    return meal_repo.delete_meal(int(meal_id))

def meal_eaten(meal_repo: MealRepo, meal_id: int):

    eaten_status = meal_repo.get_meal_eaten_status(meal_id)

    new_eaten_status = 0 if eaten_status == 1 else 1

    if meal_repo.set_meal_eaten_status(meal_id, new_eaten_status):
        return "" if new_eaten_status == 0 else "rgba(0, 255, 0, 0.15)"

    else:
        return ""
    