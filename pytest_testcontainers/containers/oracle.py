from cx_Oracle import OperationalError
from testcontainers.core.waiting_utils import wait_container_is_ready
from testcontainers.oracle import OracleDbContainer

from pytest_testcontainers.containers.base import DjangoDbContainerMixin


class OracleContainerDjango(DjangoDbContainerMixin, OracleDbContainer):
    """Oracle container with Django availability check."""

    def __init__(self, *args, **kwargs):
        """Definition of `port_to_expose` for backwards compatibility."""
        super().__init__(*args, **kwargs)
        self.port_to_expose = self.container_port

    @property
    def django_db_settings(self):
        """
        Oracle settings for Django.

        Ref https://docs.djangoproject.com/en/4.2/ref/settings/#databases
        """
        return {
            'ENGINE': 'django.db.backends.oracle',
            'NAME': 'xe',
            'USER': 'system',
            'PASSWORD': 'oracle',
        }

    @wait_container_is_ready(OperationalError)
    def _connect(self):
        super()._connect()
