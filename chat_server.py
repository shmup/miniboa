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

from miniboa.async import PortAuthority

IDLE_TIMEOUT = 300
CLIENT_LIST = []
SERVER_RUN = True


def on_connect(client):

    """Function to handle new connections."""

    broadcast('%s joins the conversation.' % client.addrport() )
    CLIENT_LIST.append(client)
    client.send("Welcome to the Chat Server")

       
def on_disconnect(client):
    
    """Function to handle lost connections."""

    CLIENT_LIST.remove(client)
    broadcast('%s leaves the conversation.' % client.addrport() )
    

def kick_idle():

    """Tests for idle clients and disconnects."""    

    global CLIENT_LIST  
    ## Who hasn't been typing?
    for client in CLIENT_LIST:
        if client.idle() > IDLE_TIMEOUT:
            print('-- Kicking idle lobby client from %s' % 
                client.addrport())
            client.active = False


def process_clients():

    """Check each client for input."""

    for client in CLIENT_LIST:
        if client.active and client.cmd_ready:
            ## If the client sends input echo it to the chat room
            chat(client)


def broadcast(msg):

    """Send msg to every client."""

    global CLIENT_LIST
    for client in CLIENT_LIST:
        client.send(msg)


def chat(speaker):

    """Echo whatever client types to everyone."""

    global SERVER_RUN
    msg = speaker.get_command()
    for client in CLIENT_LIST:
        if client == speaker:
            client.send('You say, %s' % msg)
        else:
            client.send('%s says, %s' % (speaker.addrport(), msg))

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

    ## Socket Setup
    address = ''
    port = 6666
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind((address, port))
        server_socket.listen(5)
    except socket.error, e:
        print "Unable to create the server socket:", e
        sys.exit(1)
    
    ## Create the connection manager with our server socket
    ## and a function to call with new connections and one
    ## to call with lost connections.
    port_authority = PortAuthority(server_socket, on_connect, on_disconnect)

    print(">> Listening for connections on port %d" % port)

    ## Server Loop
    while SERVER_RUN:
        port_authority.poll()
        kick_idle()
        process_clients()
        time.sleep(.01)

    print(">> Server shutdown.")

