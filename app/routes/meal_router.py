from fastapi import FastAPI, Request, APIRouter, Depends, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app_config import templates
from db.database import get_db
from domain.food import Food
from repositories.sqlite.food_repo import SQLiteFoodRepo
from services import food_service

router = APIRouter()

# ======= SHOW HTML =======
# --- SHOWS ADD TRACK HTML
@router.get("/meals/track", response_class=HTMLResponse)
def show_new_food_HTML(request: Request):
    return templates.TemplateResponse(
        "add-meal.html",
        {
            "request": request,
            "t": request.state.t
        }
    )

# === FUZZY SEARCH ===
@router.get("/meals/track/search", response_class=HTMLResponse)
def food_fuzzy_search(
    request: Request,
    query: str = Query(None),
    conn = Depends(get_db)):

    repo = SQLiteFoodRepo(conn)
    foods, scores = food_service.fuzzy_search(repo, query, 10)

    return templates.TemplateResponse(
        "add-meal.html",
        {
            "request": request,
            "foods": foods,
            "scores": scores,
            "query": query,
            "t": request.state.t
        }
    )
