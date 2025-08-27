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

    # kcal_target = g["kcal_target"] + g["objective"]
    # protein_target = g["protein_percent"]/100*kcal_target/4
    # carbs_target = g["carbs_percent"]/100*kcal_target/4
    # fats_target = g["fats_percent"]/100*kcal_target/9

    # # r=remaining, e=extra
    # kcal = {
    #     "value": min(totals["kcal"], kcal_target),
    #     "r_value": max(0, kcal_target-totals["kcal"]),
    #     "objective": kcal_target,
    #     "e_value": max(0, totals["kcal"]-kcal_target),
    #     "e_r_value": max(0, kcal_target*2-totals["kcal"])
    # }

    # protein = {
    #     "value": min(totals["protein"], protein_target),
    #     "r_value": max(0, protein_target-totals["protein"]),
    #     "objective": protein_target,
    #     "e_value": max(0, totals["protein"]-protein_target),
    #     "e_r_value": max(0, protein_target*2-totals["protein"])
    # }

    # carbs = {
    #     "value": min(totals["carbs"], carbs_target),
    #     "r_value": max(0, carbs_target-totals["carbs"]),
    #     "objective": carbs_target,
    #     "e_value": max(0, totals["carbs"]-carbs_target),
    #     "e_r_value": max(0, carbs_target*2-totals["carbs"])
    # }

    # fats = {
    #     "value": min(totals["fats"], fats_target),
    #     "r_value": max(0, fats_target-totals["fats"]),
    #     "objective": fats_target,
    #     "e_value": max(0, totals["fats"]-fats_target),
    #     "e_r_value": max(0, fats_target*2-totals["fats"])
    # }

    # # t=totals, o=objectives, e=extra
    # today = {"t": totals, "kcal": kcal, "protein": protein, "carbs": carbs, "fats": fats}

    return today

def delete_meal(meal_repo: MealRepo, meal_id: int):

    return meal_repo.delete_meal(int(meal_id))
