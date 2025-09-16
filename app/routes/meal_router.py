from fastapi import FastAPI, Request, APIRouter, Depends, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app_config import templates
from db.database import get_db
from domain.food import Food
from repositories.sqlite.food_repo import SQLiteFoodRepo
from services import food_service,meals_service,user_service
from domain.meal import MealTrack
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
            "t": request.state.t,
            "selected_lan": request.state.sel_lan
        }
    )

# === FUZZY SEARCH ===
@router.get("/meals/track/search")
def food_fuzzy_search(
    request: Request,
    query: str = Query(...),
    conn = Depends(get_db)):

    print(query)

    # return None

    repo = SQLiteFoodRepo(conn)
    foods, scores = food_service.fuzzy_search(repo, query, 10)

    return foods



# ======= MEAL TRACK =======
@router.post("/meals/track/track-meal")
def track_meal(
    request: Request,
    data: MealTrack,
    conn = Depends(get_db)):

    repo = SQLiteMealRepo(conn)
    track = meals_service.track_meal(repo, data.food_id, data.quantity, data.dt)
    
    if track:
        return {"status": "ok"}

    return {"status": "failed"}
    # return templates.TemplateResponse(
    #     "add-meal.html",
    #     {
    #         "request": request,
    #         "query": query,
    #         "track": track,
    #         "t": request.state.t
    #     }
    # )

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

# ======= MEAL DELETE NO HTML RELOAD =======
@router.post("/meals/live-delete-meal")
def del_meal(
    request: Request,
    meal_id: int,
    conn = Depends(get_db)
):

    repo = SQLiteMealRepo(conn)

    ok = meals_service.delete_meal(repo, meal_id)

    if ok:
        return {"status": "ok"}

    return {"status": "failed"}



# === MEAL MARKS AS READ
@router.get("/meals/mark-as-eaten")
def mark_meal_as_eaten(
    request: Request,
    meal_id: str = Query(...),
    conn = Depends(get_db)):

    repo = SQLiteMealRepo(conn)

    return PlainTextResponse(meals_service.meal_eaten(repo, int(meal_id)))