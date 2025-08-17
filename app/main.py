from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from routes import main_router, actions_router, food_router, i18n_router
from app_config import templates
from db.migrations_control import run_migrations
from pathlib import Path
from i18n import I18n

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(main_router.router)
app.include_router(actions_router.router)
app.include_router(food_router.router)
app.include_router(i18n_router.router)

@app.on_event("startup")
def start_app():
    run_migrations()
    
