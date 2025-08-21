from domain.food import Food
from repositories.interfaces import FoodRepo
from services import fuzzy_service

def create_food(food_repo: FoodRepo, food: Food):

    if not food.name:
        raise ValueError("THE FOOD ITS NONAME")

    return food_repo.create_food(food)

def list_foods(food_repo: FoodRepo):

    return food_repo.list_foods()

def delete_food(food_repo: FoodRepo, id: int):
    return food_repo.delete_food(id)

def edit_food(food_repo: FoodRepo, food: Food):
    return food_repo.edit_food(food)

# ======= FUZZY SEARCH =======
def fuzzy_search(food_repo: FoodRepo, query: str, limit: int) -> tuple[list[Food], list[int]]:

    if query is None:
        return [], []

    foods = food_repo.list_foods()

    return fuzzy_service.fuzzy_search(query, foods, limit)