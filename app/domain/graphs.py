from pydantic import BaseModel
from enum import Enum
from dataclasses import dataclass
from datetime import date

class ChartName(str, Enum):
    weight = "weight"
    foods = "foods"
    goals = "goals"

class TimeGrouping(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"

class DefaultGraph(BaseModel):
    chart_name: ChartName = ChartName.weight
    weight_show_kcal: bool = True
    foods_selected_foods: list = [1]
    goals_show_macros: list = [False, False, False]

class LabelRequest(BaseModel):
    days: int
    time_grouping: TimeGrouping = TimeGrouping.daily

@dataclass
class GraphDaysData:
    labels: list[date]
    time_grouping: str
    days: int