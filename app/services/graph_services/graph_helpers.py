from datetime import date, timedelta
from time import time
from dateutil.relativedelta import relativedelta

labels = []
days = 0
time_grouping = "daily"


def update_labels(d: int, t_grouping: str):
    global labels, days, time_grouping

    start_t = time()
    # print(f"START: {start_t} days: {d}")
    


    labels = []

    if d==0:
        return labels

    today_date = date.today()

    if t_grouping == "daily":
        labels = [today_date - timedelta(days=d-i) for i in range(d+1)]

    elif t_grouping == "weekly":
        first_day = today_date - timedelta(days=d)
        first_day = first_day + timedelta(days=(7-first_day.weekday()))
        weeks_number = int(d/7)
        labels = [first_day + timedelta(days=7*i) for i in range(weeks_number+1)]

    elif t_grouping == "monthly":
        first_day = today_date - timedelta(days=d)
        month = date(first_day.year, first_day.month, 1)

        while month < today_date:
            labels.append(month)
            month += relativedelta(months=+1)
        

    days = d
    time_grouping = t_grouping
    labels_isoformat = [labels[i].isoformat() for i in range(len(labels))]
    # print(f"FINISH: {time()-start_t}")
    return labels_isoformat