from domain.user import UserData
from repositories.interfaces import UserRepo
from schemas.user_form import UserDataEdit
from datetime import datetime, timezone
from services.helpers import to_int, to_float


def create_default_user(user_repo: UserRepo, lan: str):

    user = user_repo.get_user(1)


    if user:
        return user

    return user_repo.create_user_minimal(lan)

def update_user_data(user_repo: UserRepo, data: UserDataEdit):

    lan = user_repo.get_user_lan(1)

    weight = get_user_last_weight(user_repo, int(data.id))

    updated_user_data = UserData(
        id=to_int(data.id),
        name=data.name,
        is_male=int(data.is_male),
        age=to_int(data.age),
        height=to_int(data.height),
        kcal_target=to_int(data.kcal_target),
        activity_level=to_float(data.activity_level),
        protein_percent=to_float(data.protein_percent),
        carbs_percent=to_float(data.carbs_percent),
        fats_percent=to_float(data.fats_percent),
        objective=to_int(data.objective),
        lan=lan,
    )

    return user_repo.edit_user(updated_user_data), weight


def get_user_by_id(user_repo: UserRepo, user_id) -> UserData:

    return user_repo.get_user(user_id)

def get_user_lan(user_repo: UserRepo, user_id):
    return user_repo.get_user_lan(user_id)

# ======= WEIGHT CONTROL =======
def track_new_weight(user_repo: UserRepo, weight: float, id: int, dt: str) -> float:

    ts_date = int(datetime.fromisoformat(dt).timestamp())

    return user_repo.track_weight(weight, id, ts_date)

def get_user_last_weight(user_repo: UserRepo, user_id: int):
    weights = user_repo.get_all_tracked_weights(user_id)

    if not weights:
        return "None"

    return max(weights, key=lambda w: w.tracked_date).weight
