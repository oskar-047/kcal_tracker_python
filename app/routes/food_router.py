from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app_config import templates
from db.database import get_db

router = APIRouter()

@router.get("/food/new", response_class=HTMLResponse)
def show_new_food_HTML(request: Request):
    return templates.TemplateResponse(
        "create-food.html",
        {
            "request": request,
        }
    )

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
            "foods": user_food_database
        }
    )

@router.get("/food/delete/{id}")
def delete_food(request: Request, id: int, conn = Depends(get_db)):
    
    conn.execute("UPDATE user_food SET is_deleted = 1 WHERE id = ?", (id,))

    conn.commit()

    return RedirectResponse(url="/food/list", status_code=303)