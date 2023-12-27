from MySQLdb import OperationalError
from testcontainers.core.waiting_utils import wait_container_is_ready
from testcontainers.mysql import MySqlContainer

from pytest_testcontainers.containers.base import DjangoDbContainerMixin


class MySqlContainerDjango(DjangoDbContainerMixin, MySqlContainer):
    """Mysql container with Django availability check."""

    @property
    def django_db_settings(self):
        """
        Mysql settings for Django.

        Ref https://docs.djangoproject.com/en/4.2/ref/settings/#databases
        """
        return {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': self.MYSQL_DATABASE,
            'USER': self.MYSQL_USER,
            'PASSWORD': self.MYSQL_PASSWORD,
        }

    @wait_container_is_ready(OperationalError)
    def _connect(self):
        super()._connect()
