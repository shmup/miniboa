#!/usr/bin/env python
#------------------------------------------------------------------------------
#   hello_demo.py
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
