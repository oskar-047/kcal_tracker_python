from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from routes import main_router, meal_router, food_router, i18n_router, user_router, statistics_router
from db.migrations_control import run_migrations
from pathlib import Path
from repositories.sqlite.user_repo import SQLiteUserRepo
from db.session import db_conn
from services import i18n_service
from i18n import I18n

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(main_router.router)
app.include_router(meal_router.router)
app.include_router(food_router.router)
app.include_router(i18n_router.router)
app.include_router(user_router.router)
app.include_router(statistics_router.router)

i18n = I18n(Path("i18n_conf"))

@app.on_event("startup")
def start_app():
    run_migrations()


# ======= MIDDLEWARE ======= 
@app.middleware("http")
async def middleware(request: Request, call_next):
    with db_conn() as conn:

        repo = SQLiteUserRepo(conn)

        t = i18n_service.get_t(repo)
        request.state.t = t

        request.state.i18n_en = i18n._load("en")
        request.state.i18n_es = i18n._load("es")

        response = await call_next(request)
        return response

