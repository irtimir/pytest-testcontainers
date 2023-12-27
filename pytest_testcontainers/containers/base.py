from typing import Dict

from django.db import ConnectionHandler


class DjangoDbContainerMixin(object):
    """Base class container with Django availability check."""

    @property
    def django_db_settings(self) -> Dict[str, str]:
        """
        Settings for django database.

        Define the settings for the database that will be used
        for the availability check.
        """
        raise NotImplementedError()

    def _connect(self) -> None:
        host = self.get_container_host_ip()
        if host == 'localhost':
            host = '127.0.0.1'
        ConnectionHandler({
            'default': {
                'HOST': host,
                'PORT': self.get_exposed_port(self.port_to_expose),
                **self.django_db_settings,
            },
        }).create_connection('default').connect()
