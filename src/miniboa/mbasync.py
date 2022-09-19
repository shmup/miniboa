# -*- coding: utf-8 -*-
"""
Handle Asynchronous Telnet Connections.
"""

import logging
import select
import socket
import sys

from .telnet import ConnectionLost
from .telnet import TelnetClient

# Cap sockets to 512 on Windows because winsock can only process 512 at time
# Cap sockets to 1000 on UNIX because you can only have 1024 file descriptors
MAX_CONNECTIONS = 500 if sys.platform == 'win32' else 1000

LOG = logging.getLogger(__name__)


# Dummy Connection Handlers
def _on_connect(client):
    """
    Placeholder new connection handler.
    """
    LOG.info("++ Opened connection to {}, sending greeting...".format(
        client.addrport()))
    client.send("Hello, my friend. Stay awhile and listen.\n")


def _on_disconnect(client):
    """
    Placeholder lost connection handler.
    """
    LOG.info("-- Lost connection to %s".format(client.addrport()))


# Telnet Server
class TelnetServer(object):
    """
    Poll sockets for new connections and sending/receiving data from clients.
    """

    def __init__(self,
                 port=7777,
                 address='',
                 on_connect=_on_connect,
                 on_disconnect=_on_disconnect,
                 max_connections=MAX_CONNECTIONS,
                 timeout=0.05,
                 client_class=None,
                 socket_family=None,
                 encoding='cp1252'):
        """
        Create a new Telnet Server.

        port -- Port to listen for new connection on.  On UNIX-like platforms,
            you made need root access to use ports under 1025.

        address -- Address of the LOCAL network interface to listen on.  You
            can usually leave this blank unless you want to restrict traffic
            to a specific network device.  This will usually NOT be the same
            as the Internet address of your server.

        on_connect -- function to call with new telnet connections

        on_disconnect -- function to call when a client's connection dies,
            either through a terminated session or client.active being set
            to False.

        max_connections -- maximum simultaneous the server will accept at once

        timeout -- amount of time that Poll() will wait from user input
            before returning.  Also frees a slice of CPU time.

        # Make sure client_class is a subclass of TelnetClient to ensure it
        # will work fine.
        client_class -- the client class to use when accepting new connections.
            If None, the built-in TelnetClient will be used.

        socket_family -- the server socket family to use (typically one
            of AF_INET, or AF_INET6 or AF_UNIX). If None then
            AF_INET will be used.
        """

        if client_class and not issubclass(client_class, TelnetClient):
            raise TypeError('client_class must be a subclass of TelnetClient')

        self.port = port
        self.address = address
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.max_connections = min(max_connections, MAX_CONNECTIONS)
        self.timeout = timeout
        self.client_class = client_class or TelnetClient
        self.encoding = encoding

        if socket_family is None:
            socket_family = socket.AF_INET
        server_socket = socket.socket(socket_family, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_socket.bind((address, port))
            server_socket.listen(5)
        except socket.error as err:
            LOG.critical("Unable to create the server socket: " + str(err))
            raise

        self.server_socket = server_socket
        self.server_fileno = server_socket.fileno()

        # Dictionary of active clients,
        # key = file descriptor, value = self.client_class (see miniboa.telnet)
        self.clients = {}

    def stop(self):
        """
        Disconnects the clients and shuts down the server
        """
        for clients in self.client_list():
            clients.sock.close()
        self.server_socket.close()

    def client_count(self):
        """
        Returns the number of active connections.
        """
        return len(self.clients)

    def client_list(self):
        """
        Returns a list of connected clients.
        """
        return self.clients.values()

    def poll(self):
        """
        Perform a non-blocking scan of recv and send states on the server
        and client connection sockets.  Process new connection requests,
        read incomming data, and send outgoing data.  Sends and receives may
        be partial.
        """
        # Build a list of connections to test for receive data pending
        recv_list = [self.server_fileno]    # always add the server

        del_list = []    # list of clients to delete after polling

        for client in self.clients.values():
            if client.active:
                recv_list.append(client.fileno)
            else:
                self.on_disconnect(client)
                del_list.append(client.fileno)

        # Delete inactive connections from the dictionary
        for client in del_list:
            del self.clients[client]

        # Build a list of connections that need to send data
        send_list = []
        for client in self.clients.values():
            if client.send_pending:
                send_list.append(client.fileno)

        # Get active socket file descriptors from select.select()
        try:
            rlist, slist, elist = select.select(recv_list, send_list, [],
                                                self.timeout)
        except select.error as err:
            # If we can't even use select(), game over man, game over
            LOG.critical("SELECT socket error '{}'".format(str(err)))
            raise

        # Process socket file descriptors with data to recieve
        for sock_fileno in rlist:

            # If it's coming from the server's socket then this is a new connection request.
            if sock_fileno == self.server_fileno:

                try:
                    sock, addr_tup = self.server_socket.accept()
                except socket.error as err:
                    LOG.error("ACCEPT socket error '{}:{}'.".format(
                        err[0], err[1]))
                    continue

                # Check for maximum connections
                if self.client_count() >= self.max_connections:
                    LOG.warning(
                        "Refusing new connection, maximum already in use.")
                    sock.close()
                    continue

                # Create the client instance
                new_client = self.client_class(sock, addr_tup, encoding=self.encoding)

                # Add the connection to our dictionary and call handler
                self.clients[new_client.fileno] = new_client
                self.on_connect(new_client)

            else:
                # Call the connection's recieve method
                try:
                    self.clients[sock_fileno].socket_recv()
                except ConnectionLost:
                    self.clients[sock_fileno].deactivate()

        # Process sockets with data to send
        for sock_fileno in slist:
            # Call the connection's send method
            self.clients[sock_fileno].socket_send()
