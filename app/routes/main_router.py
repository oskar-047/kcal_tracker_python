from fastapi import FastAPI, Request, APIRouter, Depends, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime, date
from pathlib import Path
from app_config import templates
from domain.user import UserData
from db.database import get_db
from services import user_service, meals_service
from repositories.sqlite.user_repo import SQLiteUserRepo
from repositories.sqlite.meal_repo import SQLiteMealRepo
from repositories.sqlite.food_repo import SQLiteFoodRepo
from i18n_conf.i18n_helper import detect_lan


router = APIRouter()

# ======= MAIN ROUTER =======
@router.get("/", response_class=HTMLResponse)
def root(
    request: Request, 
    dt: date | None = Query(None),
    conn = Depends(get_db)):

    user_repo = SQLiteUserRepo(conn)
    meal_repo = SQLiteMealRepo(conn)
    food_repo = SQLiteFoodRepo(conn)

    user = user_service.create_default_user(user_repo, detect_lan(request))
    meals = meals_service.list_meals(meal_repo, food_repo, dt)

    today_macros = meals_service.calculate_total_macros(user_repo, meals)

    # delete_meal_status = request.query_params.get("delete_status")
    selected_date = dt or date.today()

    selected_lan = request.state.i18n_en if user_service.get_user_lan(user_repo, 1) == "en" else request.state.i18n_es

    return templates.TemplateResponse(
        "index.html",
        {
        "request": request,
        "t": request.state.t,
        "date": selected_date,
        "user": user,
        "meals": meals,
        "today": today_macros,
        "selected_lan": selected_lan
        # "delete_meal_status": delete_meal_status
        # "days": days
        }
    )

