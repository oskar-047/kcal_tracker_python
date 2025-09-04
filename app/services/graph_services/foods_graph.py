from domain.user import UserData
from repositories.interfaces import UserRepo, MealRepo, FoodRepo
from schemas.user_form import UserDataEdit
from datetime import date, datetime, timedelta, timezone
from services.helpers import to_int, to_float
from services import meals_service
import random
# from domain.graphs import DefaultGraph

def generate_weight_graph(user_repo: UserRepo, meal_repo: MealRepo, food_repo: FoodRepo, days: int, time_grouping: str, params):
    chart_type = _get_type()
    data, weight_range, kcal_range = _get_data(user_repo, meal_repo, food_repo, days, time_grouping, 10, params[0])
    options = _get_options(weight_range, kcal_range, params[0])

    return chart_type, data, options


def _get_type():
    return "line"

def _get_data(user_repo: UserRepo, meal_repo: MealRepo, food_repo: FoodRepo, days: int, time_grouping, margin: int, show_kcal: bool):

    # Get all weight tracks
    weights = user_repo.get_all_tracked_weights(1)

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
    labels_data = []
    weight_data = []
    kcal_data = []

    # Last weight logic
    last_weight = None

    # Search the closest weight track to the range start and saves it
    reference_date = today_date - timedelta(days=days_ago)
    last_weight_date = max((w for w in daily_weights if w<reference_date), default=None)

    if last_weight_date:
        last_weight = max((w for w in daily_weights[last_weight_date]), key=lambda x:x.id).weight

    max_weight, max_kcal = -math.inf, -math.inf
    min_weight, min_kcal = math.inf, math.inf

    # Gets the daily date and kcal directly from repo
    total_kcal = meal_repo.get_daily_kcal(t_ts(today_date - timedelta(days=days_ago)), t_ts(today_date + timedelta(days=1)))

    # Create labels, weight and kcal data list
    for i in range(days_ago+1):
        today = today_date - timedelta(days=days_ago-i)

        labels_data.append(today.isoformat())

        # Stores the dict with the biggest id key
        if daily_weights[today]:
            # Appends the last track of that day to the graph data
            today_weight = max(daily_weights[today], key=lambda x:x.id).weight
            weight_data.append(today_weight)
            last_weight = today_weight

            if today_weight > max_weight:
                max_weight = today_weight

            if today_weight < min_weight:
                min_weight = today_weight

        else:
            weight_data.append(last_weight)  

        # If meals exist calculate meals total kcal and appends it, if not it appends 0

        if total_kcal[today]:
            today_kcal = total_kcal[today]
            kcal_data.append(today_kcal)

            if today_kcal > max_kcal:
                max_kcal = today_kcal
            
            if today_kcal < min_kcal:
                min_kcal = today_kcal

        else:
            kcal_data.append(None)

        #(f"{today} {max(today_weight_tracks, key=lambda x:x.id).weight}")


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
    max_weight = round(max_weight * (1 + margin/100))
    min_weight = round(min_weight * (1 - margin/100))

    max_kcal = round(max_kcal * (1 + margin/100), -2)
    min_kcal = round(min_kcal * (1 - margin/100), -2)


    # ===== WEEK LOGIC =====
    start_day = today_date - timedelta(days=days_ago)
    # Gets the number of days needed to cut (.weekdate() returns each weekday as 0-6)
    cut = (7 - start_day.weekday()) % 7
    # Cut the days needed to get to monday as first value
    labels_data_weekbase = labels_data[cut:]
    weight_data_weekbase = weight_data[cut:]
    kcal_data_weekbase = kcal_data[cut:]

    # Initialize weekly vars
    labels_data_weekly = []
    weight_data_weekly = []
    kcal_data_weekly = []

    # Get each week chunk and getting the average, then adding to the weekly data vars
    for i in range(0, len(labels_data_weekbase), 7):
        weight_chunk = weight_data_weekbase[i:i+7]
        kcal_chunk = kcal_data_weekbase[i:i+7]

        labels_data_weekly.append(labels_data_weekbase[i])

        weight_data_weekly.append(safe_avg(weight_chunk))
        kcal_data_weekly.append(safe_avg(kcal_chunk))

    # === MONTH LOGIC ===

    start_day = today_date - timedelta(days=days_ago)
    end = today_date

    # Initialize monthly vars
    labels_data_monthly = []
    weight_data_monthly = []
    kcal_data_monthly = []

    months = []
    
    y, m = start_day.year, start_day.month
    while (y, m) <= (end.year, end.month):
        months.append((y, m))
        # Appends first month day to labels
        labels_data_monthly.append(date(y, m, 1).isoformat())

        # Get the number of the days of the current month
        month_days = calendar.monthrange(y, m)[1]

        weight_chunk = [daily_w_normalized[date(y, m, d)] for d in range(1, month_days + 1)]
        kcal_chunk = [total_kcal[date(y, m, d)] for d in range(1, month_days+1)]

        weight_data_monthly.append(safe_avg(weight_chunk))
        kcal_data_monthly.append(safe_avg(kcal_chunk))

        # increment month
        if m == 12:
            y, m = y + 1, 1
        else:
            m += 1

    
    options = {
        "daily":  (labels_data, weight_data, kcal_data),
        "weekly": (labels_data_weekly, weight_data_weekly, kcal_data_weekly),
        "monthly": (labels_data_monthly, weight_data_monthly, kcal_data_monthly),
    }

    labels, dataset_weight, dataset_kcal = options[time_grouping]


    # Creates the data dict
    data = {
        "labels": labels,
        "datasets": [
            {
                "label": 'Weight',
                "data": dataset_weight,
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
                "data": dataset_kcal,
                "borderColor": "rgb(128, 255, 128)",
                "backgroundColor": "rgb(128, 255, 128)",
                "borderWidth": 2,
                "yAxisID": "y2"
            })

    return data, [min_weight, max_weight], [min_kcal, max_kcal]



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
                    "text": "KG",
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

# litle helper function to get date from timestamp
def f_ts(ts: int) -> date:
    return date.fromtimestamp(ts)

def t_ts(dt: date) -> int:
    return int(datetime.combine(dt, datetime.min.time()).timestamp())

def safe_avg(chunk):
    result = [val for val in chunk if val not in (None, 0)]
    return sum(result) / len(result) if result else None