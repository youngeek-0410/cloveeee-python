import os

from .base import *  # noqa

DEBUG = False

ALLOWED_HOSTS = [os.getenv("ALLOWED_HOSTS")]

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django_psdb_engine",
        "NAME": os.getenv("DB_NAME"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "OPTIONS": {
            "ssl": {"ca": os.getenv("MYSQL_ATTR_SSL_CA")},
            "charset": "utf8mb4",
        },
    }
}
