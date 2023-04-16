import os
import string

SHORT_LINK_LENGTH = os.getenv('SHORT_LINK_LENGTH', default=6)
BASE_URL = os.getenv('BASE_URL', default='http://127.0.0.1:5000/')
LETTERS_NUMBERS = (string.ascii_letters + string.digits)


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='YOUR_SECRET_KEY')
