from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from db.database import get_db
from repositories.sqlite.user_repo import SQLiteUserRepo
from services import i18n_service

router = APIRouter()

@router.get("/change-lan/{user_id}")
def change_lan(request: Request, user_id, conn = Depends(get_db)):
    
    repo = SQLiteUserRepo(conn)

    i18n_service.change_lan(repo)

    return RedirectResponse("/", status_code=303)
