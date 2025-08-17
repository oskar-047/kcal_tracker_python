from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from db.database import get_db

router = APIRouter()

@router.get("/change-lan/{user_id}")
def change_lan(request: Request, user_id, conn = Depends(get_db)):
    current_lan = conn.execute("SELECT * FROM user_data WHERE id=?", (user_id,)).fetchone()["lan"]

    new_lan = "es" if current_lan == "en" else "en"

    conn.execute(
    '''
    UPDATE user_data 
    SET lan=?
    WHERE id=?
    ''',
    (new_lan, user_id)
    )

    return RedirectResponse("/", status_code=303)
