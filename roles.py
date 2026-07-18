# roles.py

import random


class RoleManager:
    def __init__(self):
        self.roles = {}

    def assign_roles(self, players, mediator):
        """
        Assign roles randomly with automatic impostor count calculation.

        Parameters:
            players (list): List of player names.
            mediator (str): Mediator name (optional).

        Returns:
            dict: {player: role}
        """

        self.roles.clear()

        # Remove mediator if present
        game_players = [p for p in players if p != mediator]

        if len(game_players) < 4:
            raise ValueError("Minimum 4 players required.")

        # Automatically calculate impostor count based on player count
        if len(game_players) <= 5:
            impostor_count = 1
        elif len(game_players) <= 8:
            impostor_count = 2
        else:
            impostor_count = 3

        # Randomly choose impostors
        impostors = random.sample(game_players, impostor_count)

        # Assign roles
        for player in game_players:

            if player in impostors:
                self.roles[player] = "Impostor"
            else:
                self.roles[player] = "Crewmate"

        return self.roles

    def get_role(self, player):
        return self.roles.get(player)

    def get_roles(self):
        return self.roles

    def get_impostors(self):
        return [
            player
            for player, role in self.roles.items()
            if role == "Impostor"
        ]

    def get_crewmates(self):
        return [
            player
            for player, role in self.roles.items()
            if role == "Crewmate"
        ]

    def clear_roles(self):
        self.roles.clear()
