# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#   miniboa/async.py
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

"""Handle Asynchronous Telnet Connections."""

import socket
import select
import time
import sys

from miniboa.telnet import Telnet

## Cap sockets to 512 on Windows because winsock can only process 512 at time
if sys.platform == 'win32':
    MAX_CONNECTIONS = 512
## Cap sockets to 1000 on Linux because you can only have 1024 file descriptors
else:
    MAX_CONNECTIONS = 1000


#----------------------------------------------------------------Port Authority

class PortAuthority(object):

    """Poll sockets for new connections and sending/receiving data from 
    clients."""

    def __init__(self, server_socket, on_connect, on_disconnect):
        """
        Takes three arguments; the server socket, a function to call with
        freshly minted telnet connections, and a function to call with
        terminally ill telnet connections. 
        """

        self.server_socket = server_socket
        self.on_connect = on_connect        ## Function to handle new Telnets
        self.on_disconnect = on_disconnect
        self.server_fd = server_socket.fileno()

        ## Dictionary of active connections 
        self.fdconn = {}

    def connection_count(self):
        """Returns the number of active connections."""
        return len(self.fdconn)

    def poll(self):

        """
        Perform a non-blocking scan of recv and send states on the server
        and client connection sockets.  Process new connection requests,
        read incomming data, and send outgoing data.  Sends and receives may
        be partial.   
        """

        ## Build a list of connections to test for receive data pending
        recv_list = [self.server_fd]    # always add the server
        for client in self.fdconn.values():
            if client.active:
                recv_list.append(client.fileno)
            ## Delete inactive connections from the dictionary
            else:
                print("-- Lost connection to %s" % client.addrport())
                self.on_disconnect(client)
                del self.fdconn[client.fileno]

        ## Build a list of connections that need to send data
        send_list = []
        for client in self.fdconn.values():
            if client.send_pending:
                send_list.append(client.fileno)

        ## Get active socket file descriptors from select.select()
        try:
            rlist, slist, elist = select.select(recv_list, send_list, [], 0)
        
        except select.error, err:
            ## If we can't even use select(), game over man, game over
            print("!! FATAL SELECT error '%d:%s'!" % (err[0], err[1])) 
            sys.exit(1)

        ## Process socket file descriptors with data to recieve
        for sockfd in rlist:

            ## If it's coming from the server's socket then this is a new
            ## connection request.
            if sockfd == self.server_fd:
            
                try:
                    sock, addr_tup = self.server_socket.accept()
                    
                except socket.error, err:
                    print("!! ACCEPT error '%d:%s'." % (err[0], err[1]))  
                    continue          

                ## Check for maximum connections
                if self.connection_count() >= ( MAX_CONNECTIONS ):
                    print('?? Refusing new connection; maximum in use.') 
                    sock.close()
                    continue
                
                client = Telnet(sock, addr_tup)
                print("++ Opened connection to %s" % client.addrport())
                ## Add the connection to our dictionary
                self.fdconn[client.fileno] = client

                ## Whatever we do with new connections goes here:
                self.on_connect(client)

            else:
                ## Call the connection's recieve method
                self.fdconn[sockfd].socket_recv()
         
        ## Process sockets with data to send
        for sockfd in slist:
            ## Call the connection's send method            
            self.fdconn[sockfd].socket_send()

