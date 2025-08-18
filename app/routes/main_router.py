from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app_config import templates
from db.database import get_db
from db.helpers import get_user_from_db, create_default_user
from i18n_conf.i18n_helper import detect_lan, make_t
from i18n import I18n



router = APIRouter()

i18n = I18n(Path("i18n_conf"))

@router.get("/", response_class=HTMLResponse)
def root(request: Request, conn = Depends(get_db)):

    user = get_user_from_db(conn, 1) # Gets user from db

    # If there's no user row creates it with the browser language
    if not user:
        lan = detect_lan(request)
        user = create_default_user(lan, True)


    print(user)
    print(detect_lan(request))

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

