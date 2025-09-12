from domain.user import UserData
from domain.graphs import ChartName, GraphDaysData
from repositories.interfaces import UserRepo, MealRepo, FoodRepo
from schemas.user_form import UserDataEdit
from services.graph_services.weight_graph import generate_weight_graph
from services.graph_services import graph_helpers
from services.graph_services.foods_graph import generate_foods_graph
from domain.graphs import DefaultGraph
# from services.graph_services.goals_graph import generate_goals_graph
import random
from datetime import date, timedelta
# from domain.graphs import DefaultGraph

def get_graph(user_repo: UserRepo, meal_repo: MealRepo, food_repo: FoodRepo, req: DefaultGraph):

    ctx = GraphDaysData(
        labels=graph_helpers.labels,
        time_grouping=graph_helpers.time_grouping,
        days=graph_helpers.days
    )

    dispatch = {
        ChartName.weight: generate_weight_graph,
        ChartName.foods: generate_foods_graph#,
        # ChartName.goals: generate_goals_graph,
    }
    return dispatch[req.chart_name](user_repo, meal_repo, food_repo, ctx, req)

