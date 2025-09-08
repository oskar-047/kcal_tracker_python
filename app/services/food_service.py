from domain.food import Food
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

    edit_food = Food(
        name=food.name,
        kcal=to_int(food.kcal),
        protein=to_float(food.protein),
        carbs=to_float(food.carbs),
        fats=to_float(food.fats),
        food_id=to_int(food.food_id)
    )

    return food_repo.edit_food(edit_food)

# ======= FUZZY SEARCH =======
def fuzzy_search(food_repo: FoodRepo, query: str, limit: int) -> tuple[list[Food], list[float]]:

    if query is None:
        return [], []

    foods = food_repo.list_foods()

    return fuzzy_service.fuzzy_search(query, foods, limit)

def get_food_by_id(food_repo: FoodRepo, food_id: int) -> Food | None:
    return food_repo.get_food_by_id(food_id)