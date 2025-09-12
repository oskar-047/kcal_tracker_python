from sqlite3 import Date
from pydantic import BaseModel
from datetime import date

class Meal(BaseModel):
        id: int | None = None
        food_id: int
        quantity: int
        tracked_date: int
        meal_type: int | None = None
        eaten: int = 0
        
class MealTrack(BaseModel):
        food_id: int
        quantity: int
        dt: date