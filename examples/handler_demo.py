# -*- coding: utf-8 -*-
"""
Example of using on_connect and on_disconnect handlers.
"""

import logging
from miniboa import TelnetServer

CLIENTS = []


def my_on_connect(client):
    """
    Example on_connect handler.
    """
    client.send('You connected from %s\n' % client.addrport())
    if CLIENTS:
        client.send('Also connected are:\n')
        for neighbor in CLIENTS:
            client.send('%s\n' % neighbor.addrport())
    else:
        client.send('Sadly, you are alone.\n')
    CLIENTS.append(client)


def my_on_disconnect(client):
    """
    Example on_disconnect handler.
    """
    CLIENTS.remove(client)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    server = TelnetServer()
    server.on_connect = my_on_connect
    server.on_disconnect = my_on_disconnect

    logging.info("Starting server on port {}. CTRL-C to interrupt.".format(
        server.port))
    while True:
        server.poll()
