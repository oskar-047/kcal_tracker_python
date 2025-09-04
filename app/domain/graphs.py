from pydantic import BaseModel
from enum import Enum

class ChartName(str, Enum):
    weight = "weight"
    foods = "foods"
    goals = "goals"

class TimeGrouping(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"

class DefaultGraph(BaseModel):
    days: int
    chart_name: ChartName = ChartName.weight
    time_grouping: TimeGrouping = TimeGrouping.daily
    weight_show_kcal: bool = True
    foods_selected_foods: list = [1]
    goals_show_macros: list = [False, False, False]
