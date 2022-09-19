import sys
import socket

PYTHON_2 = sys.version_info < (3, )


class TestTelnetServer:

    def test_telnet_server(self, server, clients):
        client = socket.socket()
        client.connect(('127.0.0.1', 7777))
        server.poll()

        # test that we have one connected client
        assert len(clients) == 1

        clients[len(clients) - 1].send("test")
        server.poll()
        data = client.recv(4)

        # test that we received the correct data
        if PYTHON_2:
            assert data == "test"
        else:
            assert data.decode("utf-8") == "test"
