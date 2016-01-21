# -*- coding: utf-8 -*-

from miniboa import TelnetServer

world = """
~~~...........^^^...
~~~~.........^^^....
~~~~~~........^^^^..
~~~~~...........^^^^
~~~.................
....................
....................
....................
"""


class Player:
    def __init__(self, client):
        self.client = client
        self.state = 'new'
        self.name = None
        self.queue = []

    def process_input(self):
        command = None

        if self.client.cmd_ready:
            command = self.client.get_command().strip()

        if self.state != 'live':
            if self.state == 'new':
                self.state = 'get_name'
                self.client.send("What is your name?\n")
            elif command and self.state == 'get_name':
                self.name = command
                self.client.send("Welcome {}!\n".format(self.name))
                self.state = 'live'
        elif self.state == 'live':
            if command is not None:
                self.queue.append(command)

            if len(self.queue):
                return self.queue.pop()


class World:
    def __init__(self):
        self.players = {}
        self.zone = Zone('earth')
        self.updates = []

    def add_player(self, client):
        print("Adding player: {}".format(client.fileno))
        self.players[client.fileno] = Player(client)

    def del_player(self, client):
        print("Removing player: {}".format(client.fileno))
        del self.players[client.fileno]

    def poll(self):
        for key, player in self.players.items():
            update = player.process_input()
            if update:
                self.updates.append((key, update))

        self.update()

    def update(self):
        updates = self.updates
        self.updates = []

        for update in updates:
            (key, cmd) = update
            cmd = cmd.strip().split(' ')
            command = cmd[0]
            modifiers = cmd[1:]
            self.process_update(key, command, modifiers)

    def process_update(self, key, command, modifiers):
        if command == 'look':
            self.zone.display()


class Zone:
    def __init__(self, name):
        self.name = name
        self.rooms = []
        self.build(world)

    def build(self, data):
        lines = data.split()
        for line in lines:
            map_row = []
            for c in line:
                map_row.append(Room(c))
            self.rooms.append(map_row)

    def display(self):
        for row in self.rooms:
            print("".join([x.color + x.symbol for x in row]))


class Room:
    def __init__(self, symbol, color=None):
        self.symbol = symbol
        self.players = []
        self.items = []
        self.color = color

        if self.color is None:
            if symbol == ".":
                self.color = '\033[0;32m'
            elif symbol == "~":
                self.color = '\033[0;34m'
            else:
                self.color = '\033[0;31m'


if __name__ == "__main__":

    world = World()

    server = TelnetServer(
            port=1334,
            address='',
            on_connect=lambda p: world.add_player(p),
            on_disconnect=lambda p: world.del_player(p),
            timeout=0.05
    )

    while True:
        server.poll()
        world.poll()
