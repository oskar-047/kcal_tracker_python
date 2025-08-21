from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app_config import templates
from domain.user import UserData
from db.database import get_db
from services import user_service
from repositories.sqlite.user_repo import SQLiteUserRepo
from i18n_conf.i18n_helper import detect_lan


router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def root(request: Request, conn = Depends(get_db)):

    repo = SQLiteUserRepo(conn)
    lan = detect_lan(request)
    
    user = user_service.create_default_user(repo, lan)

    print(user)

    return templates.TemplateResponse(
        "index.html",
        {
        "request": request,
        "today": {"kcal": 0, "protein": 0, "carbs": 0, "fats": 0},
        "t": request.state.t,
        "user": user
        # "days": days
        }
    )

