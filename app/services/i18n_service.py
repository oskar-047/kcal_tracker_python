from repositories.interfaces import UserRepo
from pathlib import Path
from i18n import I18n
from i18n_conf.i18n_helper import make_t

i18n = I18n(Path("i18n_conf"))

def get_t(user_repo: UserRepo):

    user_lan = user_repo.get_user_lan(1)

    return make_t(i18n, lan)
