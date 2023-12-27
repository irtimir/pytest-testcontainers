from psycopg2 import OperationalError
from testcontainers.core.waiting_utils import wait_container_is_ready
from testcontainers.postgres import PostgresContainer

from pytest_testcontainers.containers.base import DjangoDbContainerMixin


class PostgresContainerDjango(DjangoDbContainerMixin, PostgresContainer):
    """Postgres container with Django availability check."""

    @property
    def django_db_settings(self):
        """
        Postgres settings for Django.

        Ref https://docs.djangoproject.com/en/4.2/ref/settings/#databases
        """
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': self.POSTGRES_DB,
            'USER': self.POSTGRES_USER,
            'PASSWORD': self.POSTGRES_PASSWORD,
        }

    @wait_container_is_ready(OperationalError)
    def _connect(self):
        super()._connect()
