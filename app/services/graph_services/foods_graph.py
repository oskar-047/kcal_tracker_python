from domain.user import UserData
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

def generate_foods_graph(user_repo: UserRepo, meal_repo: MealRepo, food_repo: FoodRepo, ctx, params):
    data, range = _get_data(user_repo, meal_repo, food_repo, ctx.labels, ctx.time_grouping, ctx.days, params[0], params[1])
    options = _get_options(range)

    return data, options


def _get_data(user_repo: UserRepo, meal_repo: MealRepo, food_repo: FoodRepo, labels: list, time_grouping: str, days: int, show_kcal: bool, food_list: bool): #pyright: ignore[reportRedeclaration]

    # Get all weight tracks
    food_list: list[int] = [499, 497, 496]

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
    start_date_ts = t_ts(start_date)

    food_names, daily_tracks = meal_repo.get_meals_by_foods(start_date_ts, today_date_ts, food_list)#pyright: ignore
    
    # Creates the data dict
    data = {
        "labels": labels,
        "datasets": []
    }

    # Mins and Maxes for kcal
    max_kcal = -math.inf
    min_kcal = math.inf

    for k, v in food_names.items():

        food_dataset = []

        # If time grouping == daily
        if time_grouping == "daily":
            for today in labels:
                if daily_tracks[today][k]:
                    today_kcal = daily_tracks[today][k]["kcal"]
                    # Calculate max and min
                    max_kcal = today_kcal if today_kcal > max_kcal else max_kcal
                    min_kcal = today_kcal if today_kcal < min_kcal else min_kcal
                    food_dataset.append(today_kcal)
                else:
                    food_dataset.append(None)
                
        # If time grouping == weekly
        elif time_grouping == "weekly":
            # Iterate over the weeks
            for week in labels:
                kcal_weekly_chunk = []
                # Iterate over the week_days
                for i in range(7):
                    today = week+timedelta(days=i)
                    if daily_tracks[today][k]:
                        kcal_weekly_chunk.append(daily_tracks[today][k]["kcal"])
                
                week_kcal_avg = safe_avg(kcal_weekly_chunk)
                if week_kcal_avg is not None:
                    max_kcal = max(week_kcal_avg, max_kcal)
                    min_kcal = min(week_kcal_avg, min_kcal)
                food_dataset.append(week_kcal_avg)
                

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
                        kcal_monthly_chunk.append(daily_tracks[today][k]["kcal"])

                # Calculate mins and max and append data to dataset
                month_kcal_avg = safe_avg(kcal_monthly_chunk)
                if month_kcal_avg is not None:
                    max_kcal = max(month_kcal_avg, max_kcal)
                    min_kcal = min(month_kcal_avg, min_kcal) 
                food_dataset.append(month_kcal_avg) 


        color = f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})"

        data["datasets"].append({
                "label": v,
                "data": food_dataset,
                "borderColor": color,
                "borderWidth": 2,
                "backgroundColor": color,
                "yAxisID": "y1"
            })         

    return data, [0, 3200]

def _get_options(range: list):

    options = {
        "responsive": True,
        "scales": {
            "y1": {
                "beginAtZero": True,
                "min": range[0],
                "max": range[1],
                "title": {
                    "display": True,
                    "text": "KCAL",
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