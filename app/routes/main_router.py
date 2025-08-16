from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app_config import templates
from db.database import get_db

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def root(request: Request, conn = Depends(get_db)):

    user_food_database = conn.execute(
        '''
        SELECT * FROM user_food
        '''
    ).fetchall()

    return templates.TemplateResponse(
        "index.html",
        {
        "request": request,
        "today": {"kcal": 0, "protein": 0, "carbs": 0, "fats": 0},
        "foods": user_food_database
        # "days": days
        }
    )

