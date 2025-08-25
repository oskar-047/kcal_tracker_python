from fastapi import FastAPI, Request, APIRouter, Depends, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app_config import templates
from db.database import get_db
from schemas.user_form import UserDataEdit
from repositories.sqlite.user_repo import SQLiteUserRepo
from services import user_service

router = APIRouter()

# ======= SHOW HTML =======
# --- SHOWS USER CONF HTML
@router.get("/user/show-info", response_class=HTMLResponse)
def show_user_conf_HTML(request: Request, conn = Depends(get_db)):
    
    repo = SQLiteUserRepo(conn)

    user = user_service.get_user_by_id(repo, 1)
    weight = user_service.get_user_last_weight(repo, 1)
    print(weight)
    
    return templates.TemplateResponse(
        "user-conf.html",
        {
            "request": request,
            "weight": weight,
            "user": user,
            "t": request.state.t
        }
    )

@router.post("/user/update-data", response_class=HTMLResponse)
def update_user_data(
    request: Request,
    user_data = Depends(UserDataEdit.as_form),
    conn = Depends(get_db)):

    repo = SQLiteUserRepo(conn)
    updated_user, weight = user_service.update_user_data(repo, user_data)

    return templates.TemplateResponse(
        "user-conf.html",
        {
            "request": request, 
            "user": updated_user, 
            "weight": weight,
            "t": request.state.t
        }
    )