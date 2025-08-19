from pydantic import BaseModel

class UserData(BaseModel):
        id: int | None = None
        name: str | None = None
        height: int | None = None
        birthdate: int | None = None
        is_male: bool | None = None
        activity_level: int | None = None
        protein_percent: float | None = None
        carbs_percent: float | None = None
        fats_percent: float | None = None
        objective: int | None = None
        lan: str | None = None

class UserWeight(BaseModel):
        user_id: int
        weight: float
        date: int