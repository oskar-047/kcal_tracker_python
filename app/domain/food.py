from pydantic import BaseModel

class Food(BaseModel):
    id: int | None = None
    name: str
    kcal: int
    protein: float
    carbs: float
    fats: float
    food_id: int | None = None
    color: str = "#000000"
    favorite: bool = False
    is_default: bool = False

    class Config:
        extra = "ignore"


