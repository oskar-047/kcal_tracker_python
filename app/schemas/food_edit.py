from pydantic import BaseModel
from fastapi import Form
from datetime import date

class FoodEdit(BaseModel):
    name: str
    kcal: str
    protein: str
    carbs: str
    fats: str
    food_id: str
    is_default: int
    color: str
    favorite: int

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        kcal: str = Form(...),
        protein: str = Form(...),
        carbs: str = Form(...),
        fats: str = Form(...),
        food_id: str = Form(...),
        is_default: str = Form(...),
        color: str = Form(...),
        favorite: str = Form(...)
    ):

        d = locals().copy()
        d.pop("cls")
        return cls(**d)