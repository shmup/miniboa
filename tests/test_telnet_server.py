import sys
import socket
from miniboa import TelnetServer

PYTHON_2 = sys.version_info < (3,)
CLIENTS = []


def test_telnet_server():

    server = TelnetServer(
        port=7777,
        address='',
        on_connect=lambda x: CLIENTS.append(x),
        timeout=.05)

    client = socket.socket()
    client.connect(('127.0.0.1', 7777))
    server.poll()

    # test that we have one connected client
    assert len(CLIENTS) == 1

    CLIENTS[0].send("test")
    server.poll()
    data = client.recv(4)

    # test that we received the correct data
    if PYTHON_2:
        assert data == "test"
    else:
        assert data.decode("utf-8") == "test"
