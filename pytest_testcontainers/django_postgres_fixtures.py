import functools

import pytest

from pytest_testcontainers.containers.postgres import PostgresContainerDjango


@pytest.fixture(scope='session')
def dj_postgres_container_factory(django_db_container_factory):
    """Fixture to use PostgresContainerDjango."""
    return functools.partial(
        django_db_container_factory,
        docker_container_cls=PostgresContainerDjango,
    )
