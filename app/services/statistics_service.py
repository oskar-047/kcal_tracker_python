from domain.user import UserData
from domain.graphs import ChartName
from repositories.interfaces import UserRepo, MealRepo, FoodRepo
from schemas.user_form import UserDataEdit
from services.graph_services.weight_graph import generate_weight_graph
from services.graph_services.foods_graph import generate_foods_graph
# from services.graph_services.goals_graph import generate_goals_graph
import random
# from domain.graphs import DefaultGraph


def get_graph(user_repo: UserRepo, meal_repo: MealRepo, food_repo: FoodRepo, days: int, name: str, time_grouping: str, params: list):

    dispatch = {
        ChartName.weight: generate_weight_graph,
        ChartName.foods: generate_foods_graph#,
        # ChartName.goals: generate_goals_graph,
    }
    return dispatch[name](user_repo, meal_repo, food_repo, days, time_grouping, params)
