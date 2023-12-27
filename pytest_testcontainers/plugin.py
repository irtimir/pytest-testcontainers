import functools
import typing
from typing import TYPE_CHECKING, Callable, Generator, TypeVar

import pytest
from _pytest.fixtures import FixtureLookupError  # noqa: WPS436
from testcontainers.arangodb import ArangoDbContainer
from testcontainers.azurite import AzuriteContainer
from testcontainers.core.container import DockerContainer
# from testcontainers.clickhouse import ClickHouseContainer
from testcontainers.elasticsearch import ElasticSearchContainer
from testcontainers.google import PubSubContainer
# from testcontainers.kafka import KafkaContainer
# from testcontainers.keycloak import KeycloakContainer
from testcontainers.localstack import LocalStackContainer
# from testcontainers.minio import MinioContainer
from testcontainers.mongodb import MongoDbContainer
from testcontainers.mssql import SqlServerContainer
from testcontainers.mysql import MariaDbContainer, MySqlContainer
# from testcontainers.neo4j import Neo4jContainer
from testcontainers.nginx import NginxContainer
# from testcontainers.opensearch import OpenSearchContainer
from testcontainers.oracle import OracleDbContainer
from testcontainers.postgres import PostgresContainer
# from testcontainers.rabbitmq import RabbitMqContainer
# from testcontainers.redis import RedisContainer
from testcontainers.selenium import BrowserWebDriverContainer

pytest_plugins = []

try:
    import django  # noqa: WPS433
except ImportError:
    pass
else:
    pytest_plugins.append('pytest_testcontainers.django_fixtures')

if TYPE_CHECKING:
    DockerContainerType = TypeVar('DockerContainerType', bound=DockerContainer)


@pytest.fixture(scope='session')
def container_factory():
    """
    Base container factory

    Setup:
    * create container
    * call before start container callback
    * start container
    * call after start container callback

    Teardown:
    * stop container
    """
    cnt: typing.Optional[DockerContainerType] = None

    def factory(
        docker_container_cls,
        before_start_cb=None,
        after_start_cb=None,
        *args,
        **kwargs,
    ):
        nonlocal cnt  # noqa: WPS420
        container = docker_container_cls(*args, **kwargs)
        if before_start_cb is not None:
            before_start_cb(container)
        container.start()
        if after_start_cb is not None:
            after_start_cb(container)
        cnt = container
        return container

    yield factory

    if cnt is not None:
        cnt.stop()


@pytest.fixture(scope='session')
def postgres_container_factory(
    request: pytest.FixtureRequest,
    container_factory,
) -> Callable[..., Generator['DbContainerType', None, None]]:
    """
    Postgres docker container factory.

    The most suitable fixture will be selected, if django is installed,
    then the postgres container with django integration will be selected.

    Setup: start postgres container
    Teardown: stop postgres container
    """
    try:  # try finding an already declared fixture with that name
        yield request.getfixturevalue('dj_postgres_container_factory')
    except FixtureLookupError:
        # fixture not found, we are the only fixture named `postgres_container`
        yield functools.partial(
            container_factory,
            docker_container_cls=PostgresContainer,
        )


@pytest.fixture(scope='session')
def postgres_container(
    postgres_container_factory: Callable[..., 'DockerContainerType'],
) -> 'DockerContainerType':
    """
    Postgres container with default settings.

    Suitable for most cases
    """
    return postgres_container_factory()


@pytest.fixture(scope='session')
def arangodb_container_factory(container_factory):
    """Fixture to use ArangoDbContainer."""
    return functools.partial(
        container_factory,
        docker_container_cls=ArangoDbContainer,
    )


@pytest.fixture(scope='session')
def arangodb_container(arangodb_container_factory):
    """Arangodb container fixture."""
    return arangodb_container_factory()


@pytest.fixture(scope='session')
def azurite_container_factory(container_factory):
    """Fixture to use AzuriteContainer."""
    return functools.partial(
        container_factory,
        docker_container_cls=AzuriteContainer,
    )


@pytest.fixture(scope='session')
def azurite_container(azurite_container_factory):
    """Azurite container fixture."""
    return azurite_container_factory()


# @pytest.fixture(scope='session')
# def clickhouse_container_factory(container_factory):
#     return functools.partial(
#         container_factory,
#         docker_container_cls=ClickHouseContainer,
#     )
#
#
# @pytest.fixture(scope='session')
# def clickhouse_container(clickhouse_container_factory):
#     return clickhouse_container_factory()


@pytest.fixture(scope='session')
def elasticsearch_container_factory(container_factory):
    """Fixture to use ElasticSearchContainer."""
    return functools.partial(
        container_factory,
        docker_container_cls=ElasticSearchContainer,
    )


@pytest.fixture(scope='session')
def elasticsearch_container(elasticsearch_container_factory):
    """Elasticsearch container fixture."""
    return elasticsearch_container_factory()


@pytest.fixture(scope='session')
def google_pubsub_container_factory(container_factory):
    """Fixture to use PubSubContainer."""
    return functools.partial(
        container_factory,
        docker_container_cls=PubSubContainer,
    )


@pytest.fixture(scope='session')
def google_pubsub_container(google_pubsub_container_factory):
    """Google PubSub container fixture."""
    return google_pubsub_container_factory()


# @pytest.fixture(scope='session')
# def kafka_container_factory(container_factory):
#     return functools.partial(
#         container_factory,
#         docker_container_cls=KafkaContainer,
#     )
#
#
# @pytest.fixture(scope='session')
# def kafka_container(kafka_container_factory):
#     return kafka_container_factory()


# @pytest.fixture(scope='session')
# def keycloak_container_factory(container_factory):
#     return functools.partial(
#         container_factory,
#         docker_container_cls=KeycloakContainer,
#     )
#
#
# @pytest.fixture(scope='session')
# def keycloak_container(keycloak_container_factory):
#     return keycloak_container_factory()


@pytest.fixture(scope='session')
def localstack_container_factory(container_factory):
    """Fixture to use LocalStackContainer."""
    return functools.partial(
        container_factory,
        docker_container_cls=LocalStackContainer,
    )


@pytest.fixture(scope='session')
def localstack_container(localstack_container_factory):
    """Localstack container fixture."""
    return localstack_container_factory()


@pytest.fixture(scope='session')
def mongodb_container_factory(container_factory):
    """Fixture to use MongoDbContainer."""
    return functools.partial(
        container_factory,
        docker_container_cls=MongoDbContainer,
    )


@pytest.fixture(scope='session')
def mongodb_container(mongodb_container_factory):
    """Mongodb container fixture."""
    return mongodb_container_factory()


@pytest.fixture(scope='session')
def mssql_container_factory(container_factory):
    """Fixture to use SqlServerContainer."""
    return functools.partial(
        container_factory,
        docker_container_cls=SqlServerContainer,
    )


@pytest.fixture(scope='session')
def mssql_container(mssql_container_factory):
    """Mssql container fixture."""
    return mssql_container_factory()


@pytest.fixture(scope='session')
def mysql_container_factory(request, container_factory):
    """
    Mysql container factory.

    If django available:
        Returns `dj_mysql_container_factory` fixture.
    Else:
        Returns `MySqlContainer` factory.
    """
    try:  # try finding an already declared fixture with that name
        return request.getfixturevalue('dj_mysql_container_factory')
    except FixtureLookupError:
        # fixture not found, we are the only fixture named `postgres_container`
        return functools.partial(
            container_factory,
            docker_container_cls=MySqlContainer,
        )


@pytest.fixture(scope='session')
def mysql_container(mysql_container_factory):
    """Mysql container fixture."""
    return mysql_container_factory()


@pytest.fixture(scope='session')
def mariadb_container(mysql_container_factory):
    """Mariadb container fixture."""
    return mysql_container_factory(image='mariadb:latest')


# @pytest.fixture(scope='session')
# def neo4j_container_factory(container_factory):
#     return functools.partial(
#         container_factory,
#         docker_container_cls=Neo4jContainer,
#     )
#
#
# @pytest.fixture(scope='session')
# def neo4j_container(neo4j_container_factory):
#     return neo4j_container_factory()


@pytest.fixture(scope='session')
def nginx_container_factory(container_factory):
    """Fixture to use NginxContainer."""
    return functools.partial(
        container_factory,
        docker_container_cls=NginxContainer,
    )


@pytest.fixture(scope='session')
def nginx_container(nginx_container_factory):
    """Nginx container fixture."""
    return nginx_container_factory()


@pytest.fixture(scope='session')
def oracle_container_factory(request, container_factory):
    """
    Oracle container factory.

    If django available:
        Returns `dj_oracle_container_factory` fixture.
    Else:
        Returns `OracleDbContainer` factory.
    """
    try:  # try finding an already declared fixture with that name
        return request.getfixturevalue('dj_oracle_container_factory')
    except FixtureLookupError:
        # fixture not found, we are the only fixture named `postgres_container`
        return functools.partial(
            container_factory,
            docker_container_cls=OracleDbContainer,
        )


@pytest.fixture(scope='session')
def oracle_container(oracle_container_factory):
    """Oracle container fixture."""
    return oracle_container_factory()


# @pytest.fixture(scope='session')
# def rabbitmq_container_factory(container_factory):
#     return functools.partial(
#         container_factory,
#         docker_container_cls=RabbitMqContainer,
#     )
#
#
# @pytest.fixture(scope='session')
# def rabbitmq_container(rabbitmq_container_factory):
#     return rabbitmq_container_factory()


# @pytest.fixture(scope='session')
# def redis_container_factory(container_factory):
#     return functools.partial(
#         container_factory,
#         docker_container_cls=RedisContainer,
#     )
#
#
# @pytest.fixture(scope='session')
# def redis_container(redis_container_factory):
#     return redis_container_factory()


@pytest.fixture(scope='session')
def selenium_container_factory(container_factory):
    """Fixture to use BrowserWebDriverContainer."""
    return functools.partial(
        container_factory,
        docker_container_cls=BrowserWebDriverContainer,
    )


@pytest.fixture(scope='session')
def selenium_container(selenium_container_factory):
    """Selenium container fixture."""
    return selenium_container_factory()
