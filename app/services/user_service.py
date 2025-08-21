from domain.user import UserData
from repositories.interfaces import UserRepo

def create_default_user(user_repo: UserRepo, lan: str):

    user = user_repo.get_user(1)


    if user:
        return user

    return user_repo.create_user_minimal(lan)