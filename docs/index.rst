===============================
Miniboa: a simple Telnet server
===============================

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

-------------
Telnet Server
-------------

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
    Greetings from Miniboa!  Now it's time to add your code.

Initialization arguments for TelnetServer are:

- **server** = TelnetServer(port=8888, address='127.0.0.1', on_connect=my_connect_handler, on_disconnect=my_disconnect_handler)
- **port** - the network port you want the server to listen for new connections on. You should be aware that on Linux, port numbers 1024 and below are restricted for use by normal users. The default is port 7777.
- **address** - this is the address of the local network interface you wish the server to listen on. You can usually omit this parameter (or pass an empty string; '') which causes it to listen on any viable NIC. Unless your server is directly connected to the Internet (doubtful today) do not set this to the Internet IP address of your server. The default is an empty string.
- **on_connect** - this is the handler function that is called by the server when a new connection is made. It will be passed the Client object of the new user. The default is a placeholder function that greets the visitor and prints their connection info to stdout.
- **on_disconnect** - this is the hander function that is called by the server when connection is lost. It will be passed the Client object of the lost user. The default is a placeholder function that prints the lost connection info to stdout.
- **timeout** - length of time to wait for user input during each poll(). Default is 5 milliseconds.

The follow Server Properties can be read from:

- port - port the server is listening to.
- address - address of the local network interface the server is listening to. See the explanation of this parameter above.

You can set or change these after creating the server:

- **on_connect** - handler function for new connections.
- **on_disconnect** - handler function for lost connections.
- **timeout** - length of time to wait on user input during a pol(). Default is .005 seconds. Increasing this value also lowers CPU usage.
- **Server** Methods
- **poll()** - this is where the server looks for new connections and processes existing connection that need to send and/or receive blocks of data with the players. A call to this method needs to be made from within your program's game loop.
- **connection_count()** - returns the number of current connections.
- **client_list()** - returns a list of the current client objects.

Here's a simple example with custom on_connect() and on_disconnect() handlers:

.. code-block:: python 
    from miniboa import TelnetServer

    CLIENTS = []

    def my_on_connect(client):
        """Example on_connect handler."""
        client.send('You connected from %s\r\n' % client.addrport())
        if CLIENTS:
            client.send('Also connected are:\r\n')
            for neighbor in CLIENTS:
                client.send('%s\r\n' % neighbor.addrport())
        else:
            client.send('Sadly, you are alone.\r\n')
        CLIENTS.append(client)


    def my_on_disconnect(client):
        """Example on_disconnect handler."""
        CLIENTS.remove(client)

    server = TelnetServer()
    server.on_connect=my_on_connect
    server.on_disconnect=my_on_disconnect

    print "\n\nStarting server on port %d.  CTRL-C to interrupt.\n" % server.port
    while True:
        server.poll()

--------------
Telnet Clients
--------------

Client objects are instances of the TelnetClient class from miniboa.telnet. These are a mixture of a state machine, send & receive buffers, and some convenience methods. They are created when a new connection is detected by the TelnetServer and passed to your on_connect() and on_disconnect() handler functions. Your application will probably maintain a list (or some other kind of reference) to these clients so it's important to delete references in your on_disconnect handler or else dead ones will not get garbage collected.

The client buffers user's input and breaks it into lines of text that can be retrieved using the get_command() method.

**Client Properties**

- **active** - boolean value, True if the client is in good health. Setting this to False will cause the TelnetServer to drop the user (and then call your on_disconnect() function with that client).
- **cmd_ready** - this is set to True whenever the user enters some text and then presses the enter key. The line of text can be obtained by calling the get_command() method.
- **bytes_sent** - number of bytes sent to the client since the session began.
- **bytes_received** - number of bytes received from the client since the session began.
- **columns** - Number of columns the client's window supports. This is set to a default of 80 and then modified if request_naws() is called AND the player's client supports NAWS (Negotiate about Window Size). See RFC 1073.
- **rows** - number of rows the client's window supports. This is set to a default of 24 and then modified if request_naws() is called AND the player's client supports NAWS (Negotiate about Window Size). See RFC 1073.
- **address** - the client's remote IP address.
- **port** - the client's port number.
- **terminal_type** - the client's terminal type. Defaults to 'unknown terminal' and changed if request_terminal_type() is called AND the player's client supports this IAC. See RFC 779.

**Client Methods**

- **send()** - append the given text to the client's send buffer which is actually transmitted during a TelnetServer.poll() call. Python newlines ('\n') are automatically converted to '\r\n' (carriage return + new line) per Telnet specifications.
- **send_cc()** - send the given text and convert caret codes into ANSI color sequences. See the Wiki for a list of caret codes. See http://code.google.com/p/miniboa/wiki/CaretCodes for a list.
- **send_wrapped** - send the given text wrapped to the user's terminal width. Requires a prior NAWS sequence. Caret codes are converted to ANSI sequences via send_cc().
- **get_command()** - returns a line of user input or None (if nothing). You can also check the property client.cmd_ready to see if input is available. Carriage returns and newlines are stripped.
- **addrport()** - returns the client's IP address and port number in the format '127.0.0.1:12345'.
- **idle()** - returns the number of seconds since the user last typed.
- **duration()** - returns the number of seconds since the user first connected.
- **password_mode_on()** - request the user's client not to locally echo keystrokes. It seems that Microsoft's telnet.exe is broken in that you cannot resume local echoing once turned off.
- **password_mode_off()** - request the user's client to resume local echo of keystrokes.
- **request_do_sga()** - Request distant end to Suppress Go-Ahead. See RFC 858.
- **request_will_echo()** - Tell the distant end that we would like to echo their text. See RFC 857.
- **request_wont_echo()** - Tell the distant end that we would like to stop echoing their text. See RFC 857.
- **request_naws()** - Request to Negotiate About Window Size. Results will be stored in the properties client.columns and client.rows. See RFC 1073.
- **request_terminal_type()** - Begins the Telnet negotiations to request the terminal type from the distant end. Result will be stored in the property client.terminal_type. See RFC 779. See http://code.google.com/p/miniboa/wiki/TerminalTypes for a list of terminal types that I've found so far.

Keep in mind that request_naws() and request_terminal_type() are not instantaneous. When you call them, a special byte sequence is added to the client's send buffer and wont actually transmit until the next server.poll() call. Then the distant end has to reply (assuming they support them) and those replies require another server.poll() to process the socket's input.

----------
Hello Demo
----------

.. code-block:: python

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

------------
Handler Demo
------------

.. code-block:: python

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
        server.on_connect=my_on_connect
        server.on_disconnect=my_on_disconnect

        logging.info("Starting server on port {}. CTRL-C to interrupt.".format(server.port))
        while True:
            server.poll()

----------------
Chat Server Demo
----------------

.. code-block:: python

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
                logging.info("Kicking idle lobby client from {}".format(client.addrport()))
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
            timeout = .05
            )

        logging.info("Listening for connections on port {}. CTRL-C to break.".format(telnet_server.port))

        # Server Loop
        while SERVER_RUN:
            telnet_server.poll()        # Send, Recv, and look for new connections
            kick_idle()                 # Check for idle clients
            process_clients()           # Check for client input

        logging.info("Server shutdown.")
