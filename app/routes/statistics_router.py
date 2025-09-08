from fastapi import FastAPI, Request, APIRouter, Depends, Form, Query, Body
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app_config import templates
from db.database import get_db
from schemas.user_form import UserDataEdit
from repositories.sqlite.user_repo import SQLiteUserRepo
from repositories.sqlite.meal_repo import SQLiteMealRepo
from repositories.sqlite.food_repo import SQLiteFoodRepo
from services import user_service, statistics_service
from services.graph_services.graph_helpers import update_labels
from datetime import date
from domain.graphs import DefaultGraph, LabelRequest

router = APIRouter()

# ======= SHOW HTML =======
# === SHOW weight track html
@router.get("/statistics/weight/track", response_class=HTMLResponse)
def show_weight_track_HTML(
    request: Request,
    conn = Depends(get_db)
):

    user_repo = SQLiteUserRepo(conn)

    last_weight = user_service.get_user_last_weight(user_repo, 1)

    dt = date.today()
    

    return templates.TemplateResponse(
        "weight-track.html",
        {
            "request": request,
            "weight": last_weight,
            "date": dt,
            "t": request.state.t
        }
    )

# === SHOW weight graph html
@router.get("/statistics/main", response_class=HTMLResponse)
def show_statistics_HTML(
    request: Request,
    conn = Depends(get_db)
):

    return templates.TemplateResponse(
        "weight-log.html",
        {
            "request": request,
            "t": request.state.t
        }
    )

# Returns graph data
@router.post("/statistics/show-chart")
def send_graph_data_weight(
    request: Request,
    graph_request: DefaultGraph,
    conn = Depends(get_db)
):
    user_repo = SQLiteUserRepo(conn)
    meal_repo = SQLiteMealRepo(conn)
    food_repo = SQLiteFoodRepo(conn)

    params = [graph_request.weight_show_kcal, graph_request.foods_selected_foods, graph_request.goals_show_macros]
    data, options = statistics_service.get_graph(user_repo, meal_repo, food_repo, graph_request.chart_name, params)

    return {"data": data, "options": options}


@router.post("/statistics/update-labels")
def make_labels(
    request: Request,
    req: LabelRequest
):

    return update_labels(req.days, req.time_grouping)