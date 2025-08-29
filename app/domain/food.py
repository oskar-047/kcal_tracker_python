from pydantic import BaseModel

class Food(BaseModel):
    id: int | None = None
    name: str
    kcal: int
    protein: float
    carbs: float
    fats: float
    food_id: int | None = None

    class Config:
        extra = "ignore"

