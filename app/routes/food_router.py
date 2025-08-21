from fastapi import FastAPI, Request, APIRouter, Depends, Form
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
# --- SHOWS CREATE FOOD HTML
@router.get("/food/new", response_class=HTMLResponse)
def show_new_food_HTML(request: Request):
    return templates.TemplateResponse(
        "create-food.html",
        {
            "request": request,
            "t": request.state.t
        }
    )

# --- SHOWS FOOD HTML
@router.get("/food/list", response_class=HTMLResponse)
def show_new_food_HTML(request: Request, conn = Depends(get_db)):

    repo = SQLiteFoodRepo(conn)

    foods = food_service.list_foods(repo)

    return templates.TemplateResponse(
        "list-foods.html",
        {
            "request": request,
            "t": request.state.t,
            "foods": foods
        }
    )

# ======= ACTIONS =======
# === CREATE ===
@router.post("/food/create-food", response_class=HTMLResponse)
def create_food(
    request: Request, 
    conn = Depends(get_db),
    name: str = Form(...),
    kcal: int = Form(...),
    protein: float = Form(...),
    carbs: float = Form(...),
    fats: float = Form(...)):

    food = Food(name=name, kcal=kcal, protein=protein, carbs=carbs, fats=fats)

    repo = SQLiteFoodRepo(conn)

    added_food = food_service.create_food(repo, food)

    return templates.TemplateResponse(
        "create-food.html",
        {
            "request": request,
            "t": request.state.t,
            "food": added_food
        }
    )

# === DELETE ===
@router.post("/food/delete-food")
def delete_food(
    request: Request,
    food_id: str = Form(...),
    conn = Depends(get_db),
):
    repo = SQLiteFoodRepo(conn)

    ok = food_service.delete_food(repo, int(food_id))
    if not ok:
        raise HTTPException(status_code=404, detail="Food not found")

    return RedirectResponse(url="/food/list", status_code=303)


# === FUZZY SEARCH ===
