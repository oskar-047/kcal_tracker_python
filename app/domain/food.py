from pydantic import BaseModel

class Food(BaseModel):
    id: int | None = None
    name: str
    kcal: int
    protein: float
    carbs: float
    fats: float

    class Config:
        extra = "ignore"

