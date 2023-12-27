import functools

import pytest

from pytest_testcontainers.containers.mysql import MySqlContainer


@pytest.fixture(scope='session')
def dj_mysql_container_factory(django_db_container_factory):
    """Fixture to use MySqlContainer."""
    return functools.partial(
        django_db_container_factory,
        docker_container_cls=MySqlContainer,
    )
