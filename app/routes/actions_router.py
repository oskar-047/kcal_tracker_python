from fastapi import FastAPI, Request, APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app_config import templates
from db.database import get_db

router = APIRouter()


@router.post("/create-new-food", response_class=HTMLResponse)
def create_food(
    request: Request, 
    conn = Depends(get_db),
    name: str = Form(...),
    kcal: int = Form(...),
    protein: float = Form(...),
    carbs: float = Form(...),
    fats: float = Form(...)):

    conn.execute(
        '''
        INSERT INTO user_food (name, kcal, protein, carbs, fats) 
        VALUES (?, ?, ?, ?, ?)
        ''',
        (name, kcal, protein, carbs, fats,)
    )

    food = (name, kcal, protein, carbs, fats,)

    return templates.TemplateResponse(
        "create-food.html",
        {
            "request": request,
            "food": food
        }
    )

