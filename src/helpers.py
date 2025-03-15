import random
import string
from src import constants


def generate_email(length=8):
    return 'test' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length)) + '@mail.com'


def generate_password(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_name(length=6):
    return 'User' + ''.join(random.choices(string.ascii_letters, k=length))


def get_ingredients(length=3):
    return random.choices(constants.INGREDIENTS_LIST, k=length)


def generate_string(length=21):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
