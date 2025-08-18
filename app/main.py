from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from routes import main_router, actions_router, food_router, i18n_router
from app_config import templates
from db.migrations_control import run_migrations
from pathlib import Path
from i18n import I18n
import sqlite3
from db.database import DB_PATH
from i18n_conf.i18n_helper import get_user_lan, make_t

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

i18n = I18n(Path("i18n_conf"))

app.include_router(main_router.router)
app.include_router(actions_router.router)
app.include_router(food_router.router)
app.include_router(i18n_router.router)

@app.on_event("startup")
def start_app():
    run_migrations()


    
@app.middleware("http")
async def middleware(request: Request, call_next):
    lan = get_user_lan(1)
        
    t = make_t(i18n, lan)

    request.state.t = t

    response = await call_next(request)
    return response

