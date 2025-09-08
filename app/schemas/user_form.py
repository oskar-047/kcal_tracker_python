from pydantic import BaseModel
from fastapi import Form
from datetime import date
        
class UserDataEdit(BaseModel):
    id: int
    name: str | None = None
    is_male: str | None = None
    age: str | None = None
    height: str | None = None
    kcal_target: str | None = None
    activity_level: str | None = None
    protein_percent: str | None = None
    carbs_percent: str | None = None
    fats_percent: str | None = None
    objective: str | None = None

    @classmethod
    def as_form(
        cls,
        id: int = Form(...),
        name: str | None = Form(None),
        is_male: str | None = Form(None),
        age: str | None = Form(None),
        height: str | None = Form(None),
        kcal_target: str | None = Form(None),
        protein_percent: str | None = Form(None),
        carbs_percent: str | None = Form(None),
        fats_percent: str | None = Form(None),
        activity_level: str | None = Form(None),
        objective: str | None = Form(None),

    ):
        # Saves on "d" a copy of all scope vars
        d = locals().copy()

        # Deletes the var cls (is not needed)
        d.pop("cls")

        # Returns the class with the arguments
        return cls(**d)