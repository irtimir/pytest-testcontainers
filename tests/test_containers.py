import pytest

from pytest_testcontainers.containers.mysql import MySqlContainerDjango
from pytest_testcontainers.containers.oracle import OracleContainerDjango
from pytest_testcontainers.containers.postgres import PostgresContainerDjango


# @pytest.fixture(autouse=True)
# def unblock_django_db(django_db_blocker):
#     with django_db_blocker.unblock():
#         yield


@pytest.mark.parametrize(
    ['container_class', 'provided', 'expected'],
    (
        (
            MySqlContainerDjango,
            {},
            {
                'ENGINE': 'django.db.backends.mysql',
                'USER': 'test',
                'NAME': 'test',
                'PASSWORD': 'test',
            },
        ),
        (
            MySqlContainerDjango,
            {
                'MYSQL_DATABASE': 'test1',
                'MYSQL_USER': 'test1',
                'MYSQL_PASSWORD': 'test1',
            },
            {
                'ENGINE': 'django.db.backends.mysql',
                'USER': 'test1',
                'NAME': 'test1',
                'PASSWORD': 'test1',
            },
        ),
        (
            OracleContainerDjango,
            {},
            {
                'ENGINE': 'django.db.backends.oracle',
                'USER': 'system',
                'NAME': 'xe',
                'PASSWORD': 'oracle',
            },
        ),
        (
            PostgresContainerDjango,
            {},
            {
                'ENGINE': 'django.db.backends.postgresql',
                'USER': 'test',
                'NAME': 'test',
                'PASSWORD': 'test',
            },
        ),
        (
            PostgresContainerDjango,
            {
                'user': 'test1',
                'password': 'test1',
                'dbname': 'test1',
            },
            {
                'ENGINE': 'django.db.backends.postgresql',
                'USER': 'test1',
                'NAME': 'test1',
                'PASSWORD': 'test1',
            },
        ),
    ),
)
def test_container_dj_settings(container_class, provided, expected):
    assert container_class(**provided).django_db_settings == expected


@pytest.mark.parametrize('container_class', [PostgresContainerDjango, MySqlContainerDjango])
def test_container_work(container_class):
    container = container_class()
    container.start()
    docker_client = container.get_docker_client()
    short_id = container.get_wrapped_container().short_id
    assert docker_client.get_container(short_id)['State'] == 'running'
    container.stop()
    with pytest.raises(RuntimeError) as e:
        docker_client.get_container(short_id)
        assert str(e) == 'could not get container with id ' + short_id
