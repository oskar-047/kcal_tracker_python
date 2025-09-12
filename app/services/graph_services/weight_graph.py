from domain.user import UserData
from domain.graphs import DefaultGraph
from repositories.interfaces import UserRepo, MealRepo, FoodRepo
from schemas.user_form import UserDataEdit
from datetime import date, datetime, time, timedelta, timezone
from services.helpers import to_int, to_float
from services import meals_service
from services.helpers import warning
from collections import defaultdict
import random
import math
import calendar
# from domain.graphs import DefaultGraph

def generate_weight_graph(user_repo: UserRepo, meal_repo: MealRepo, food_repo: FoodRepo, ctx, req: DefaultGraph):

    data, weight_range, kcal_range = _get_data(user_repo, meal_repo, food_repo, ctx.labels, ctx.time_grouping, ctx.days, req.weight_show_kcal)
    options = _get_options(weight_range, kcal_range, req.weight_show_kcal)

    return data, options

def _get_data(user_repo: UserRepo, meal_repo: MealRepo, food_repo: FoodRepo, labels: list, time_grouping: str, days: int, show_kcal: bool):

    # Get all weight tracks
    weights = user_repo.get_all_tracked_weights(1)

    # If there no weights, return empty data
    if not weights:
        warning("No weights found")
        return {"labels": labels,"datasets": []}, [0, 100], [1200, 2500]

    # Gets today day
    today_date = date.today()

    # Creates a dict where non existing keys will have [] value (empty list)
    daily_weights = defaultdict(list)
    # Fulls the dict with arrays of each day, also converts tracked_date from ts to date objects
    for w in weights:
        d = date.fromtimestamp(w.tracked_date)
        daily_weights[d].append(w)

    # Normalize daily_weights with only 1 weight per day
    daily_w_normalized = defaultdict(int)
    for k, v in daily_weights.items():
        daily_w_normalized[k] = max(v, key=lambda x:x.id).weight
    
    # How many days ago the statistic will display  
    days_ago = days

    # If days == 0 it gets the first tracked weight and starts from that date (shows all weight tracks)
    if days==0:
        first_date = min(daily_weights)
        days_ago = (today_date - first_date).days

    # Initialize all data for the chart
    weight_data = []
    kcal_data = []

    # === LAST WEIGH LOGIC ===
    # Search the closest weight track to the range start and saves it
    reference_date = today_date - timedelta(days=days_ago)
    last_weight_date = max((w for w in daily_w_normalized if w<reference_date), default=None)
    
    last_weight = daily_w_normalized[last_weight_date] if last_weight_date else None

    max_weight, max_kcal = -math.inf, -math.inf
    min_weight, min_kcal = math.inf, math.inf

    # Gets the daily date and kcal directly from repo
    total_kcal = meal_repo.get_daily_kcal(t_ts(today_date - timedelta(days=days_ago)), t_ts(today_date + timedelta(days=1)))

    # ======= DAILY LOGIC =======
    if time_grouping == "daily":
        for today in labels:
            today_w = daily_w_normalized[today]
            if today_w:
                last_weight = today_w

                # Check if today weights is more or less than max or min
                max_weight = today_w if today_w > max_weight else max_weight
                min_weight = today_w if today_w < min_weight else min_weight
            
            weight_data.append(last_weight)  

            t_kcal = total_kcal[today]
            if t_kcal:
                # Check if today kcal is more or less than max or min
                max_kcal = t_kcal if t_kcal > max_kcal else max_kcal
                min_kcal = t_kcal if t_kcal < min_kcal else min_kcal
            
            kcal_data.append(t_kcal if t_kcal else None)

    # ======= WEEK LOGIC =======
    elif time_grouping == "weekly":
        for week in labels: # iterate weeks
            weight_avg, kcal_avg = get_data_avg(week, 7, daily_w_normalized, total_kcal)
            # Calculate new max and minds
            if weight_avg:
                max_weight = weight_avg if weight_avg > max_weight else max_weight
                min_weight = weight_avg if weight_avg < min_weight else min_weight
            if kcal_avg:
                max_kcal = kcal_avg if kcal_avg > max_kcal else max_kcal
                min_kcal = kcal_avg if kcal_avg < min_kcal else min_kcal
            weight_data.append(weight_avg)
            kcal_data.append(kcal_avg)

    # ======= MONTH LOGIC =======
    elif time_grouping == "monthly":
        for month in labels: # iterate over months
            _, month_days = calendar.monthrange(month.year, month.month)
            weight_avg, kcal_avg = get_data_avg(month, month_days, daily_w_normalized, total_kcal)
            # Calculate new max and minds
            if weight_avg:
                max_weight = weight_avg if weight_avg > max_weight else max_weight
                min_weight = weight_avg if weight_avg < min_weight else min_weight
            if kcal_avg:
                max_kcal = kcal_avg if kcal_avg > max_kcal else max_kcal
                min_kcal = kcal_avg if kcal_avg < min_kcal else min_kcal
            weight_data.append(weight_avg)
            kcal_data.append(kcal_avg)

    # Check the mion/max values are not infinite
    if math.isinf(max_weight):
        max_weight = 80
    if math.isinf(min_weight):
        min_weight = 50
    if math.isinf(max_kcal):
        max_kcal = 3200
    if math.isinf(min_kcal):
        min_kcal = 1600

    # Round max and min
    max_weight = round(max_weight * (1 + 0.05))
    min_weight = round(min_weight * (1 - 0.05))

    max_kcal = round(max_kcal * (1 + 0.1), -2)
    min_kcal = round(min_kcal * (1 - 0.1), -2)

    # Creates the data dict
    data = {
        "labels": labels,
        "datasets": [
            {
                "label": 'Weight',
                "data": weight_data,
                "borderColor": "red",
                "borderWidth": 2,
                "backgroundColor": "red",
                "yAxisID": "y1"
            }            
        ]
    }

    if show_kcal:
        data["datasets"].append({
                "label": 'KCAL',
                "data": kcal_data,
                "borderColor": "rgb(128, 255, 128)",
                "backgroundColor": "rgb(128, 255, 128)",
                "borderWidth": 2,
                "yAxisID": "y2"
            })

    return data, [min_weight, max_weight], [min_kcal, max_kcal]

def get_data_avg(init_dt: date, for_range: int, weights: defaultdict[date, float], total_kcal: defaultdict[date, int]) -> tuple[float | None, float | None]:
    weight_chunk = []
    kcal_chunk = []
    for i in range(for_range):
        today = init_dt + timedelta(days=i)
        t_weight = weights[today]
        t_kcal = total_kcal[today]
        if t_weight: # append today weight to chunk if exists
            weight_chunk.append(t_weight)
        if t_kcal: # append today kcal to chunk if exists
            kcal_chunk.append(t_kcal)

    weight_avg = safe_avg(weight_chunk) # make averages
    kcal_avg = safe_avg(kcal_chunk)
    return weight_avg, kcal_avg

def _get_options(weight_range: list, kcal_range: list, show_kcal: bool):

    options = {
        "responsive": True,
        "scales": {
            "y1": {
                "beginAtZero": True,
                "min": weight_range[0],
                "max": weight_range[1],
                "title": {
                    "display": True,
                    "text": "Quantity (KG)",
                    "color": "rgba(255, 255, 255, 0.3)"
                },
                "grid": {
                    "color": "rgba(255, 255, 255, 0.3)"
                },
                "ticks": {
                    "color": "rgba(255, 255, 255, 0.3)"
                }
            },
            "x": {
                "title": {
                    "display": True,
                    "text": "Days",
                    "color": "rgba(255, 255, 255, 0.3)"
                },
                "grid": {
                    "color": "rgba(255, 255, 255, 0.3)"
                },
                "ticks": {
                    "color": "rgba(255, 255, 255, 0.3)"
                }
            }
        }
    }

    if show_kcal:
        options["scales"]["y2"] = {
            "beginAtZero": True,
            "min": kcal_range[0],
            "max": kcal_range[1],
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
            },
            "position": "right"
        }

    return options

# litle helper function to get date from timestamp and other
def f_ts(ts: int) -> date:
    return date.fromtimestamp(ts)

def t_ts(dt: date) -> int:
    return int(datetime.combine(dt, datetime.min.time()).timestamp())

def safe_avg(chunk):
    result = [val for val in chunk if val not in (None, 0)]
    return sum(result) / len(result) if result else None