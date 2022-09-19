import pytest
from miniboa import TelnetServer

CLIENTS = []

@pytest.fixture(scope="function")
def server():
    return TelnetServer(port=7777,
                        address='',
                        on_connect=lambda x: CLIENTS.append(x),
                        timeout=.05)


@pytest.fixture(scope="function")
def utf8_server():
    return TelnetServer(port=7777,
                        address='',
                        on_connect=lambda x: CLIENTS.append(x),
                        timeout=.05,
                        encoding='utf-8')

@pytest.fixture(scope="function")
def clients():
    return CLIENTS
