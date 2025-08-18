from fastapi import Request
import sqlite3
from db.database import DB_PATH
from i18n import I18n

def detect_lan(request: Request) -> str:
    # When the user enters the web, the browser automatically send a header on 
    # the http request, here the script reads that header

    # This line tries to get the header, if it can't it will save "" inside the var
    header = request.headers.get("accept-language", "")
    if not header:
        header = "en"

    lang_code = header.split(",")[0]
    return lang_code.split("-")[0]

def get_user_lan(id: str) -> str:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT lan FROM user_data WHERE id=?", (id,)).fetchone()
        return row["lan"] if row else "en"
    finally:
        conn.close()

# This function returns a function with a fixed lan used by jinja2 on the templates
def make_t(i18n: I18n, lan):
    return lambda key, **vars: i18n.t(key, lan, **vars)
