from uuid import uuid4
from random import randint


def get_group_number():
    return 0 #randint(0, 11)


def get_reward_token():
    return uuid4().hex
