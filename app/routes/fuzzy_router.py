from fastapi import FastAPI, Request, APIRouter, Depends, Form, Query, HTTPException
from db.database import get_db
from repositories.sqlite.food_repo import SQLiteFoodRepo
from services import food_service

router = APIRouter()

# Returns only listed foods from fuzzy search
@router.get("/fuzzy/food-search")
def fuzzy_food_search(
    request: Request,
    q: str,
    max: int,
    conn = Depends(get_db)
):

    repo = SQLiteFoodRepo(conn)
    foods, _ = food_service.fuzzy_search(repo, q, max)

    return foods