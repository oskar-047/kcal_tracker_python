from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app_config import templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
        "request": request,
        "today": {"kcal": 0, "protein": 0, "carbs": 0, "fats": 0}
        # "days": days
        }
    )

@router.get("/food/new", response_class=HTMLResponse)
def show_new_food_HTML(request: Request):
    return templates.TemplateResponse(
        "create-food.html",
        {
            "request": request,
        }
    )