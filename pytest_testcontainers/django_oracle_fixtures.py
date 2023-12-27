import functools

import pytest

from pytest_testcontainers.containers.oracle import OracleContainerDjango


@pytest.fixture(scope='session')
def dj_oracle_container_factory(django_db_container_factory):
    """Fixture to use OracleContainerDjango."""
    return functools.partial(
        django_db_container_factory,
        docker_container_cls=OracleContainerDjango,
    )
