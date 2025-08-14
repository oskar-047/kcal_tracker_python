from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from routes.main_router import router
from app_config import templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)