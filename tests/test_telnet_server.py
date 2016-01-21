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

    bart = socket.socket()
    bart.connect(('127.0.0.1', 7777))
    server.poll()
    CLIENTS[0].send("test")
    server.poll()
    data = bart.recv(4)

    if PYTHON_2:
        assert data == "test"
    else:
        assert data.decode("utf-8") == "test"
