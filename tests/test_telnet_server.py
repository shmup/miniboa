import sys
import socket
import pytest
from miniboa import TelnetServer
from miniboa.telnet import TelnetClient

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


class MockSocket:
    def __init__(self):
        self._recv_queue = []

    def fileno(self):
        return 999

    def queue_recv(self, data):
        self._recv_queue.append(data)

    def recv(self, size):
        return self._recv_queue.pop(0) if self._recv_queue else b''


@pytest.mark.skipif(PYTHON_2, reason="Python 3 only")
@pytest.mark.parametrize("chunk1,chunk2,expected", [
    # here we have unicode encoded as utf-8 bytes, they are in "broken" up chunks, that the first
    # read call only receives up to 'chunk1', and the second 'chunk2' -- prove that the full
    # completed sequence is received by successful use of incrementaldecoder.
    (b'caf\xc3', b'\xa9\n', 'café'),
    (b'price: \xe2', b'\x82\xac100\n', 'price: €100'),
    (b'hi \xf0\x9f', b'\x98\x80\n', 'hi 😀'),
])
def test_incremental_decoder_split_utf8(chunk1, chunk2, expected):
    mock_sock = MockSocket()
    client = TelnetClient(mock_sock, ('127.0.0.1', 12345), encoding='utf-8')

    mock_sock.queue_recv(chunk1)
    client.socket_recv()

    mock_sock.queue_recv(chunk2)
    client.socket_recv()

    assert client.cmd_ready is True
    assert client.get_command() == expected


@pytest.mark.skipif(PYTHON_2, reason="Python 3 only")
def test_encoding_change_reinitializes_decoder():
    mock_sock = MockSocket()
    client = TelnetClient(mock_sock, ('127.0.0.1', 12345), encoding='cp1252')
    assert client.encoding == 'cp1252'

    client.encoding = 'utf-8'
    assert client.encoding == 'utf-8'

    mock_sock.queue_recv(b'caf\xc3\xa9\n')
    client.socket_recv()
    assert client.get_command() == 'café'
