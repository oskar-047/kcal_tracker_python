from fastapi import FastAPI, Request, APIRouter, Depends, Form, Query, HTTPException, Body
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app_config import templates
from db.database import get_db
from domain.food import Food, FoodId
from repositories.sqlite.food_repo import SQLiteFoodRepo
from services import food_service
from schemas.food_edit import FoodEdit

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

# --- SHOWS FOOD LIST HTML
@router.get("/food/list", response_class=HTMLResponse)
def show_food_list_HTML(request: Request, conn = Depends(get_db)):

    repo = SQLiteFoodRepo(conn)

    foods = food_service.list_foods(repo)

    return templates.TemplateResponse(
        "list-foods.html",
        {
            "request": request,
            "t": request.state.t,
            "selected_lan": request.state.sel_lan
            # "foods": foods
        }
    )

# === FUZZY SEARCH ===
# Show list foods HTML with fuzzy search
@router.get("/food/list/search", response_class=HTMLResponse)
def food_fuzzy_search(
    request: Request,
    query: str = Query(None),
    conn = Depends(get_db)):

    repo = SQLiteFoodRepo(conn)
    foods, scores = food_service.fuzzy_search(repo, query, 10)

    # dt = datetime.now().replace(microsecond=0).strftime("%Y-%m-%dT%H:%M")

    return templates.TemplateResponse(
        "list-foods.html",
        {
            "request": request,
            # "date": dt,
            "foods": foods,
            "scores": scores,
            "query": query,
            "t": request.state.t
        }
    )

# === SHOWS FOOD EDIT HTML WITH DATA
@router.get("/food/edit-food", response_class=HTMLResponse)
def show_edit_food_HTML(
    request: Request, 
    food_id: str = Query(...),
    conn = Depends(get_db)):

    repo = SQLiteFoodRepo(conn)

    food = food_service.get_food_by_id(repo, food_id)

    print(food)

    return templates.TemplateResponse(
        "edit-food.html",
        {
            "request": request,
            "t": request.state.t,
            "food": food
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

# === EDIT ===
@router.post("/food/edit-food")
def edit_food(
    request: Request,
    food = Depends(FoodEdit.as_form),
    conn = Depends(get_db)
):
    repo = SQLiteFoodRepo(conn)

    new_food = food_service.edit_food(repo, food)

    return RedirectResponse(
        url="/food/list", status_code=303
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


# === FOOD COLOR EDIT ===
@router.get("/food/edit-color")
def edit_food_color(
    request: Request,
    food_id: str,
    color: str,
    conn = Depends(get_db)
):
    repo = SQLiteFoodRepo(conn)

    ok = food_service.edit_color(repo, color, food_id)

    if ok:
        return {"status": "ok"}
    
    return {"status": "failed"}

# === PIN FOOD ITEM ===
@router.post("/food/pin-food")
def pin_food(
    request: Request,
    food_id: FoodId,
    conn = Depends(get_db)
): 
    repo = SQLiteFoodRepo(conn)

    ok = food_service.pin_food(repo, food_id)

    return {"status": "ok"} if ok else {"status": "failed"}

@router.get("/food/get-pined")
def get_pined(
    request: Request,
    conn = Depends(get_db)
): 
    repo = SQLiteFoodRepo(conn)

    food = food_service.get_pined_food(repo)

    return food