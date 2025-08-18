from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app_config import templates
from db.database import get_db

router = APIRouter()

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

    user_food_database = conn.execute(
        '''
        SELECT * FROM user_food
        '''
    ).fetchall()

    return templates.TemplateResponse(
        "list-foods.html",
        {
            "request": request,
            "t": request.state.t,
            "foods": user_food_database
        }
    )


