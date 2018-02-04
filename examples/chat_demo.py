# -*- coding: utf-8 -*-
"""
Chat Room Demo for Miniboa.
"""

import logging
from miniboa import TelnetServer

IDLE_TIMEOUT = 300
CLIENT_LIST = []
SERVER_RUN = True


def on_connect(client):
    """
    Sample on_connect function.
    Handles new connections.
    """
    logging.info("Opened connection to {}".format(client.addrport()))
    broadcast("{} joins the conversation.\n".format(client.addrport()))
    CLIENT_LIST.append(client)
    client.send("Welcome to the Chat Server, {}.\n".format(client.addrport()))


def on_disconnect(client):
    """
    Sample on_disconnect function.
    Handles lost connections.
    """
    logging.info("Lost connection to {}".format(client.addrport()))
    CLIENT_LIST.remove(client)
    broadcast("{} leaves the conversation.\n".format(client.addrport()))


def kick_idle():
    """
    Looks for idle clients and disconnects them by setting active to False.
    """
    # Who hasn't been typing?
    for client in CLIENT_LIST:
        if client.idle() > IDLE_TIMEOUT:
            logging.info("Kicking idle lobby client from {}".format(
                client.addrport()))
            client.active = False


def process_clients():
    """
    Check each client, if client.cmd_ready == True then there is a line of
    input available via client.get_command().
    """
    for client in CLIENT_LIST:
        if client.active and client.cmd_ready:
            # If the client sends input echo it to the chat room
            chat(client)


def broadcast(msg):
    """
    Send msg to every client.
    """
    for client in CLIENT_LIST:
        client.send(msg)


def chat(client):
    """
    Echo whatever client types to everyone.
    """
    global SERVER_RUN
    msg = client.get_command()
    logging.info("{} says '{}'".format(client.addrport(), msg))

    for guest in CLIENT_LIST:
        if guest != client:
            guest.send("{} says '{}'\n".format(client.addrport(), msg))
        else:
            guest.send("You say '{}'\n".format(msg))

    cmd = msg.lower()
    # bye = disconnect
    if cmd == 'bye':
        client.active = False
    # shutdown == stop the server
    elif cmd == 'shutdown':
        SERVER_RUN = False


if __name__ == '__main__':

    # Simple chat server to demonstrate connection handling via the
    # async and telnet modules.
    logging.basicConfig(level=logging.DEBUG)

    # Create a telnet server with a port, address,
    # a function to call with new connections
    # and one to call with lost connections.
    telnet_server = TelnetServer(
        port=7777,
        address='',
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        timeout=.05)

    logging.info("Listening for connections on"
                 " port {}. CTRL-C to break.".format(telnet_server.port))

    # Server Loop
    while SERVER_RUN:
        telnet_server.poll()    # Send, Recv, and look for new connections
        kick_idle()    # Check for idle clients
        process_clients()    # Check for client input

    logging.info("Server shutdown.")
