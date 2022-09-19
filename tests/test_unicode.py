import sys
import socket

PYTHON_2 = sys.version_info < (3, )


class TestTelnetServer:

    def test_unicode(self, utf8_server, clients):
        client = socket.socket()
        client.connect(('127.0.0.1', 7777))
        utf8_server.poll()

        # Send a u2052 and u2044 character
        clients[len(clients) - 1].send("⁒⁄")
        utf8_server.poll()
        data = client.recv(8)

        # test that we received the correct data
        if PYTHON_2:
            assert data == "⁒⁄"
        else:
            assert data.decode("utf-8") == "⁒⁄"
