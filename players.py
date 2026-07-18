# players.py

class PlayerManager:
    def __init__(self):
        self.players = []

    def add_player(self, name):
        """Add a player if the name is valid and not already present."""
        name = name.strip()

        if not name:
            return False, "Player name cannot be empty."

        if name.lower() in [player.lower() for player in self.players]:
            return False, "Player already exists."

        self.players.append(name)
        return True, f"{name} added successfully."

    def remove_player(self, name):
        """Remove a player."""
        if name in self.players:
            self.players.remove(name)
            return True, f"{name} removed successfully."

        return False, "Player not found."

    def get_players(self):
        """Return all players."""
        return self.players.copy()

    def clear_players(self):
        """Remove all players."""
        self.players.clear()

    def player_count(self):
        """Return number of players."""
        return len(self.players)

    def player_exists(self, name):
        """Check whether player exists."""
        return name in self.players