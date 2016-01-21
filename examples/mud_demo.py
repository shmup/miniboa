# -*- coding: utf-8 -*-

from miniboa import TelnetServer


class Player:
    def __init__(self, client):
        self.client = client
        self.state = 'new'
        self.name = None

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
                print(command)


class World:
    def __init__(self):
        self.players = {}

    def add_player(self, client):
        print("Adding player: {}".format(client.fileno))
        self.players[client.fileno] = Player(client)

    def del_player(self, client):
        print("Removing player: {}".format(client.fileno))
        del self.players[client.fileno]

    def poll(self):
        for _, player in self.players.items():
            player.process_input()
        pass


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
