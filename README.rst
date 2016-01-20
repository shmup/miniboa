===================================================================
Miniboa: a simple Telnet server
===================================================================

-----
What?
-----

Miniboa is a bare-bones Telnet server to use as the base for a MUD or similar interactive server. Miniboa has several nice features for this type of application.

--------
Features
--------

- Asynchronous - no waiting on player input or state.
- Single threaded - light on resources with excellent performance.
- Runs under your game loop - you decide when to poll for data.
- Supports 1000 users under Linux and 512 under Windows (untested).
- Miniboa is compatable with both Python 2.6, 2.7, and 3.

-----------
Quick Start
-----------

To use Miniboa, you create a Telnet Server object listening at a specified port number. You have to provide two functions for the server; the first is a handler for new connections and the second is the handler for lost connections. These handler functions are passed Telnet Client objects -- these are your communication paths to and from the individual player's MUD client.

For example, let's say Mike and Joe connect to your MUD server. Telnet Server will call your on_connect() function with Mike's Telnet Client object, and then again with Joe's Telnet Client object. If Mike's power goes out, Telnet Server will call your on_disconnect() function with Mike's Telnet Client object (same exact one).


Telnet servers are instances of the TelnetServer class from miniboa.async. Creating a Telnet Server is pretty simple. In fact, you can run one with the following three lines of code:

.. code-block:: python

    from miniboa import TelnetServer
    server = TelnetServer()
    while True: server.poll()

This will launch a server listening on the default port, 7777, that accepts Telnet connections and sends a simple greeting;

.. code-block:: bash

    $ telnet localhost 7777
    Trying 127.0.0.1...
    Connected to localhost.
    Escape character is '^]'.
    Hello, my friend. Stay awhile and listen.

Further documentation can be `found here <https://github.com/shmup/miniboa/blob/master/docs/index.rst/>`_.

=========
Copyright
=========

.. code-block:: bash

    Copyright 2009 Jim Storch
    Copyright 2015 Carey Metcalfe
    Copyright 2016 Joseph Schilz
    Copyright 2016 Jared Miller
