from domain.food import Food, FoodId
from repositories.interfaces import FoodRepo
from schemas.food_edit import FoodEdit
from services import fuzzy_service
from services.helpers import to_int, to_float

def create_food(food_repo: FoodRepo, food: Food):

    if not food.name:
        raise ValueError("THE FOOD ITS NONAME")

    return food_repo.create_food(food)

def list_foods(food_repo: FoodRepo):

    return food_repo.list_foods()

def delete_food(food_repo: FoodRepo, id: int):
    return food_repo.delete_food(id)

def edit_food(food_repo: FoodRepo, food: FoodEdit):

    edit_food:Food = Food(
        name=food.name,
        kcal=to_int(food.kcal),
        protein=to_float(food.protein),
        carbs=to_float(food.carbs),
        fats=to_float(food.fats),
        food_id=to_int(food.food_id),
        is_default=to_int(food.is_default),
        color=food.color
    )

    if edit_food.is_default == 1:
        food_repo.unset_all_default_food()

    return food_repo.edit_food(edit_food)

def edit_color(food_repo: FoodRepo, color: str, food_id: str) -> bool:
    return food_repo.edit_food_color(color, int(food_id))
    

# ======= FUZZY SEARCH =======
def fuzzy_search(food_repo: FoodRepo, query: str, limit: int) -> tuple[list[Food], list[float]]:

    if query is None:
        return [], []

    foods = food_repo.list_foods()

    return fuzzy_service.fuzzy_search(query, foods, limit)

def get_food_by_id(food_repo: FoodRepo, food_id: int) -> Food | None:
    return food_repo.get_food_by_id(food_id)

# === DEFAULT FOOD SYSTEM ===
def pin_food(food_repo: FoodRepo, food_id: FoodId):
    ok = food_repo.unset_all_default_food()

    if(ok):
        return food_repo.set_default_food(food_id.food_id)
    else:
        return ok

def get_pined_food(food_repo: FoodRepo) -> FoodId | None:
    return food_repo.get_default_food()