#!/usr/bin/env python
#------------------------------------------------------------------------------
#   chat_server.py
#   Copyright 2009 Jim Storch
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain a
#   copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#------------------------------------------------------------------------------

import socket
import time

from miniboa.async import TelnetServer

IDLE_TIMEOUT = 300
CLIENT_LIST = []
SERVER_RUN = True


#----------------------------------------------------Sample on_connect Function

def on_connect(client):

    """
    Function to handle new connections.
    """

    print "++ Opened connection to %s" % client.addrport()
    broadcast('%s joins the conversation.\r\n' % client.addrport() )
    CLIENT_LIST.append(client)
    client.send("Welcome to the Chat Server\r\n")


#-------------------------------------------------Sample on_disconnect Function

def on_disconnect(client):

    """
    Function to handle lost connections.
    """

    print "-- Lost connection to %s" % client.addrport()
    CLIENT_LIST.remove(client)
    broadcast('%s leaves the conversation.\r\n' % client.addrport() )


#----------------------Sample function that tests the idle time of every client

def kick_idle():

    """
    Looks for idle clients and disconnects them by setting active to False.
    """

    global CLIENT_LIST
    ## Who hasn't been typing?
    for client in CLIENT_LIST:
        if client.idle() > IDLE_TIMEOUT:
            print('-- Kicking idle lobby client from %s' % client.addrport())
            client.active = False


#---------------------------------Sample function for checking for client input

def process_clients():

    """
    Check each client, if client.cmd_ready == True then there is a line of
    input available via client.get_command().
    """

    for client in CLIENT_LIST:
        if client.active and client.cmd_ready:
            ## If the client sends input echo it to the chat room
            chat(client)


#----------------------------------Sample function to send text to every client

def broadcast(msg):

    """Send msg to every client."""

    global CLIENT_LIST
    for client in CLIENT_LIST:
        client.send(msg)


#Sample function that handles the client commands detected by process_clients()

def chat(speaker):

    """Echo whatever client types to everyone."""

    global SERVER_RUN
    msg = speaker.get_command()
    print '%s says, "%s"' % (speaker.addrport(), msg)
    for client in CLIENT_LIST:
        if client == speaker:
            client.send('You say, %s\r\n' % msg)
        else:
            client.send('%s says, %s\r\n' % (speaker.addrport(), msg))

    ## bye = disconnect
    if msg.strip() == 'bye':
        client.active = False

    ## shutdown == stop the server
    if msg.strip() == 'shutdown':
        SERVER_RUN = False


#------------------------------------------------------------------------------
#       Main
#------------------------------------------------------------------------------

if __name__ == '__main__':

    """
    Simple chat server to demonstrate connection handling via the
    async and telnet modules.
    """

    ## Create a telnet server with a port, address,
    ## a function to call with new connections
    ## and one to call with lost connections.

    telnet_server = TelnetServer(
        port=7777,
        address='',
        on_connect=on_connect,
        on_disconnect=on_disconnect
        )

    print(">> Listening for connections on port %d" % telnet_server.port)

    ## Server Loop
    while SERVER_RUN:
        telnet_server.poll()        ## Send, Recv, and look for new connections
        kick_idle()                 ## Check for idle clients
        process_clients()           ## Check for client input
        time.sleep(.01)             ## Give up a sliver of system time

    print(">> Server shutdown.")
