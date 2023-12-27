import functools
from typing import TYPE_CHECKING

import pytest
from django.conf import settings

pytest_plugins = []

try:
    import MySQLdb
except ImportError:
    pass
else:
    pytest_plugins.append('pytest_testcontainers.django_mysql_fixtures')

try:
    import cx_Oracle
except ImportError:
    pass
else:
    pytest_plugins.append('pytest_testcontainers.django_oracle_fixtures')

try:
    import psycopg2
except ImportError:
    pass
else:
    pytest_plugins.append('pytest_testcontainers.django_postgres_fixtures')

if TYPE_CHECKING:
    from pytest_django.plugin import _DatabaseBlocker  # noqa: WPS450


def after_start_db_container(container, django_db_blocker):
    django_db_blocker.block()
    settings.DATABASES['default'].update({
        **container.django_db_settings,
        'HOST': container.get_container_host_ip(),
        'PORT': container.get_exposed_port(container.port_to_expose),
    })


@pytest.fixture(scope='session')
def django_db_container_factory(
    django_db_blocker: '_DatabaseBlocker',
    container_factory,
):
    return functools.partial(
        container_factory,
        before_start_cb=lambda _: django_db_blocker.unblock(),
        after_start_cb=functools.partial(after_start_db_container, django_db_blocker=django_db_blocker),
    )
