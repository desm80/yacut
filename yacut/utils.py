import random

from yacut.models import URLMap
from yacut.settings import LETTERS_NUMBERS, SHORT_LINK_LENGTH


def get_unique_short_id():
    """
    Создание уникальной короткой ссылки.
    """
    short_id = ''
    for i in range(int(SHORT_LINK_LENGTH)):
        short_id += random.choice(list(LETTERS_NUMBERS))
    if URLMap.query.filter_by(short=short_id).first():
        return get_unique_short_id()
    return short_id


def validate_or_create_short_id(short_id):
    """
    Проверка ввода короткой ссылки в форме и при его отсутствии вызов метода
    создания короткой ссылки.
    """
    if short_id == '' or short_id is None:
        short_id = get_unique_short_id()
    return short_id
