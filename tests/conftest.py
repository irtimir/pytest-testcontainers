import pytest

pytest_plugins = 'pytester'


@pytest.fixture
def unblock_django_db(django_db_blocker):
    with django_db_blocker.unblock():
        yield
