import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    YANDEX_DISK_AUTH_TOKEN = os.getenv('YANDEX_DISK_AUTH_TOKEN')
