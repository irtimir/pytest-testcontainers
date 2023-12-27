from os import environ

from .settings_base import *  # noqa: F401 F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "pytest_django_tests_default",
        "USER": environ.get("TEST_DB_USER", "root"),
        "PASSWORD": environ.get("TEST_DB_PASSWORD", ""),
        "HOST": environ.get("TEST_DB_HOST", "localhost"),
    },
}
