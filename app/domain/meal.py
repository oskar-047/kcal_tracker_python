from pydantic import BaseModel

class Meal(BaseModel):
        id: int | None = None
        food_id: int
        quantity: int
        tracked_date: int
        meal_type: int | None = None
        eaten: int = 0