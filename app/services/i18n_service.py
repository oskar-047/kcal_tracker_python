from fastapi import Request
from repositories.interfaces import UserRepo
from services import user_service
from pathlib import Path
from i18n import I18n
from i18n_conf.i18n_helper import make_t

i18n = I18n(Path("i18n_conf"))

def get_t(user_repo: UserRepo):

    user_lan = user_repo.get_user_lan(1)

    if not user_lan:
        return make_t(i18n, "en")

    return make_t(i18n, user_lan)

def change_lan(user_repo: UserRepo):
    current_lan = user_repo.get_user_lan(1)

    if current_lan:

        new_lan = "es" if current_lan == "en" else "en"

        return user_repo.change_user_lan(1, new_lan)

    return None
