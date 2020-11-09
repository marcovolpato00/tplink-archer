import pytest


@pytest.fixture()
def test_server():
    from .test_server import create_app_mock

    app = create_app_mock()
    return app


@pytest.fixture
def connection(test_server):
    from tplink_archer import ArcherConnection

    with test_server.run('127.0.0.1', 5000):
        connection = ArcherConnection('127.0.0.1:5000')
        connection.authenticate('admin', 'password')
    return connection
