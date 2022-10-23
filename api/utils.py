import os
from data import models


def sign_up(name, phone):
    user_list = models.User.objects.filter(name=name, phone=phone)
    if len(user_list) != 0:
        return 0
    user = models.User(name, phone)
    user.save()
    return 1


def get_secret_key():
    env_dist = os.environ
    print(env_dist)
    return env_dist['SUDOKU_JWT_KEY']


if __name__ == '__main__':
    print(get_secret_key())
