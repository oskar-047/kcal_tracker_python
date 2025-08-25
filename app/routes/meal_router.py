from fastapi import FastAPI, Request, APIRouter, Depends, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app_config import templates
from db.database import get_db
from domain.food import Food
from repositories.sqlite.food_repo import SQLiteFoodRepo
from services import food_service,meals_service
from domain.meal import Meal
from repositories.sqlite.meal_repo import SQLiteMealRepo
from datetime import datetime, date

router = APIRouter()

# ======= SHOW HTML =======
# --- SHOWS ADD TRACK HTML
@router.get("/meals/track", response_class=HTMLResponse)
def show_new_food_HTML(request: Request):
    
    dt = datetime.now().replace(microsecond=0).strftime("%Y-%m-%dT%H:%M")
    
    return templates.TemplateResponse(
        "add-meal.html",
        {
            "request": request,
            "date": dt,
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

    dt = datetime.now().replace(microsecond=0).strftime("%Y-%m-%dT%H:%M")

    return templates.TemplateResponse(
        "add-meal.html",
        {
            "request": request,
            "date": dt,
            "foods": foods,
            "scores": scores,
            "query": query,
            "t": request.state.t
        }
    )


# ======= MEAL TRACK =======
@router.post("/meals/track/track-meal", response_class=HTMLResponse)
def track_meal(
    request: Request,
    query: str = Form(None),
    food_id: str = Form(...),
    quantity: int = Form(...),
    dt: datetime = Form(...),
    conn = Depends(get_db)):

    repo = SQLiteMealRepo(conn)
    track = meals_service.track_meal(repo, food_id, quantity, dt)

    return templates.TemplateResponse(
        "add-meal.html",
        {
            "request": request,
            "query": query,
            "track": track,
            "t": request.state.t
        }
    )

# ======= MEAL DELETE =======
@router.post("/meals/delete", response_class=HTMLResponse)
def delete_meal(
    request: Request, 
    meal_id: str = Form(...),
    dt: date|None = Form(None),
    conn = Depends(get_db)):

    repo = SQLiteMealRepo(conn)

    status = meals_service.delete_meal(repo, meal_id)

    target = "/"
    if dt:
        target += f"?dt={dt.isoformat()}&delete_status={status}"
    else:
        target += f"?delete_status={status}"

    return RedirectResponse(url=target, status_code=303)