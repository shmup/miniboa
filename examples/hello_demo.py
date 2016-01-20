#!/usr/bin/env python

"""
As simple as it gets.

Launch the Telnet server on the default port and greet visitors using the
placeholder 'on_connect()' function.  Does nothing else.
"""

import logging
from miniboa import TelnetServer

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    server = TelnetServer()

    logging.info("Starting server on port {}. CTRL-C to interrupt.".format(server.port))
    while True:
        server.poll()
