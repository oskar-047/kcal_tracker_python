from domain.user import UserData
from domain.graphs import DefaultGraph, TimeGrouping
from repositories.interfaces import UserRepo, MealRepo, FoodRepo
from schemas.user_form import UserDataEdit
from datetime import date, datetime, timedelta, timezone
from services.helpers import to_int, to_float
from services import meals_service
from collections import defaultdict
import random
import math
import calendar
# from domain.graphs import DefaultGraph

def generate_foods_graph(user_repo: UserRepo, meal_repo: MealRepo, food_repo: FoodRepo, ctx, req: DefaultGraph):

    # print(req.attribute)
    display_mode = req.attribute if req.attribute != "show-kcal" and req.attribute != "none" else "quantity"

    data, v_range = _get_data(user_repo, meal_repo, food_repo, ctx.labels, ctx.time_grouping, ctx.days, req.foods_selected_foods, display_mode)
    options = _get_options(v_range, display_mode)

    return data, options


def _get_data(user_repo: UserRepo, meal_repo: MealRepo, food_repo: FoodRepo, labels: list, time_grouping: str, days: int, food_list: list[int], display_mode: str):

    # Get all weight tracks
    if not food_list:
        return {}, [0, 3200]

    # Gets today day
    today_date = date.today()
    today_date_ts = t_ts(today_date + timedelta(days=1))

    # How many days ago the statistic will display  
    days_ago = days

    # If days == 0 it gets the first tracked weight and starts from that date (shows all weight tracks)
    # if days==0:
        # first_date = min(daily_weights)
        # days_ago = (today_date - first_date).days

    start_date = today_date - timedelta(days=days_ago)
    if(time_grouping == "monthly"):
        start_date = date(start_date.year, start_date.month, 1)
    start_date_ts = t_ts(start_date)

    food_names, daily_tracks = meal_repo.get_meals_by_foods(start_date_ts, today_date_ts, food_list)#pyright: ignore
    
    # Creates the data dict
    data = {
        "labels": labels,
        "datasets": []
    }

    # Mins and Maxes for kcal
    max_v = -math.inf
    min_v = math.inf

    for k, v in food_names.items():

        food_dataset = []

        # If time grouping == daily
        if time_grouping == "daily":
            for today in labels:
                if daily_tracks[today][k]:
                    today_v = daily_tracks[today][k][display_mode]
                    # Calculate max and min
                    max_v = today_v if today_v > max_v else max_v
                    min_v = today_v if today_v < min_v else min_v
                    food_dataset.append(today_v)
                else:
                    food_dataset.append(None)
                
        # If time grouping == weekly
        elif time_grouping == "weekly":
            # Iterate over the weeks
            for week in labels:
                value_weekly_chunk = []
                # Iterate over the week_days
                for i in range(7):
                    today = week+timedelta(days=i)
                    if daily_tracks[today][k]:
                        value_weekly_chunk.append(daily_tracks[today][k][display_mode])
                
                week_value_total = sum(value_weekly_chunk) # Total system
                # week_kcal_avg = safe_avg(kcal_weekly_chunk) # Average system
                if week_value_total is not None:
                    max_v = max(week_value_total, max_v)
                    min_v = min(week_value_total, min_v)
                food_dataset.append(week_value_total)
                

        # If time grouping == monthly
        elif time_grouping == "monthly":
            # Iterate over the months
            for month in labels:
                kcal_monthly_chunk = []
                # Iterate over the month_days
                _, month_days = calendar.monthrange(month.year, month.month)
                for i in range(month_days):
                    today = month+timedelta(days=i)
                    if daily_tracks[today][k]:
                        kcal_monthly_chunk.append(daily_tracks[today][k][display_mode])

                # Calculate mins and max and append data to dataset
                month_value_total = sum(kcal_monthly_chunk) # Total system
                # month_value_avg = safe_avg(kcal_monthly_chunk) # Average system
                if month_value_total is not None:
                    max_v = max(month_value_total, max_v)
                    min_v = min(month_value_total, min_v) 
                food_dataset.append(month_value_total) 

        if math.isinf(max_v): max_v = 1500
        if math.isinf(min_v): min_v = 100

        color = f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})"

        data["datasets"].append({
                "label": v["name"],
                "data": food_dataset,
                "borderColor": v["color"],
                "borderWidth": 2,
                "backgroundColor": v["color"],
                "yAxisID": "y1"
            })         

    return data, [min_v *0.9, max_v*1.1]

def _get_options(v_range: list, display_mode: str):

    display = "KCAL" if display_mode == "kcal" else "Quantity (g)"

    options = {
        "responsive": True,
        "scales": {
            "y1": {
                "beginAtZero": True,
                "min": v_range[0],
                "max": v_range[1],
                "title": {
                    "display": True,
                    "text": display,
                    "color": "rgb(255, 255, 255, 0.3)"
                },
                "grid": {
                    "color": "rgb(255, 255, 255, 0.3)"
                },
                "ticks": {
                    "color": "rgb(255, 255, 255, 0.3)"
                }
            },
            "x": {
                "title": {
                    "display": True,
                    "text": "Days",
                    "color": "rgb(255, 255, 255, 0.3)"
                },
                "grid": {
                    "color": "rgb(255, 255, 255, 0.3)"
                },
                "ticks": {
                    "color": "rgb(255, 255, 255, 0.3)"
                }
            }
        }
    }

    return options

# litle helper function to get date from timestamp
def f_ts(ts: int) -> date:
    return date.fromtimestamp(ts)

def t_ts(dt: date) -> int:
    return int(datetime.combine(dt, datetime.min.time()).timestamp())

def safe_avg(chunk) -> float | None:
    result = [val for val in chunk if val not in (None, 0)]
    return sum(result) / len(result) if result else None