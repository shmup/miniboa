#!/usr/bin/env python
#------------------------------------------------------------------------------
#   character_demo.py
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

"""
****************************************************
THIS IS EXPERIMENTAL AND PROBABLY DOES NOT WORK YET.
****************************************************

Example of using Character Mode, where the client sends every keystroke to
our server and individual characters are available via the get_chr() method.

Technically, we're really turning line-mode off but since line-mode is the
default for every client I've seen, we'll pretend.
"""

import random

from miniboa.character_server import CharModeServer

CLIENTS = []

def my_on_connect(client):
    """
    Example on_connect handler that enables character mode.
    """
    client.send('Hello, you are connected from %s\n' % client.addrport())
    CLIENTS.append(client)


def my_on_disconnect(client):
    """
    Example on_disconnect handler.
    """
    CLIENTS.remove(client)


def process_character(client):
    """
    Silly demo of grabbing a character and echoing it back to the client.
    """
    ## Get a character
    ch = client.get_char()
    print "got %s:%d" % (ch, ord(ch))
    client.send(ch)
    ## Randomly capitalize it
#    if random.choice([True, False]):
#        client.send(char.upper())
#    else:
#        client.send(char.lower())


server = CharModeServer()
server.on_connect=my_on_connect
server.on_disconnect=my_on_disconnect

print "\n\nStarting server on port %d.  CTRL-C to interrupt.\n" % server.port
while True:
    server.poll()

    for client in CLIENTS:
        if client.char_ready:
            process_character(client)
