# voting.py

from collections import Counter


class VotingManager:
    def __init__(self):
        self.votes = {}
        self.dead_players = set()
        self.alive_players = set()

    def initialize_players(self, players):
        """
        Initialize all players as alive.
        """
        self.alive_players = set(players)
        self.dead_players = set()
        self.votes = {}

    def cast_vote(self, voter, voted_player):
        """
        Cast a vote.
        """

        if voter in self.dead_players:
            return False, f"{voter} is eliminated and cannot vote."

        if voted_player in self.dead_players:
            return False, "Cannot vote for an eliminated player."

        if voter not in self.alive_players:
            return False, "Invalid voter."

        if voted_player not in self.alive_players:
            return False, "Invalid player selected."

        # One vote per player
        self.votes[voter] = voted_player

        return True, "Vote submitted."

    def vote_count(self):
        """
        Return vote totals.
        """
        return dict(Counter(self.votes.values()))

    def eliminate_player(self):
        """
        Eliminate player with highest votes.

        Returns:
            (eliminated_player, tie)
        """

        if not self.votes:
            return None, False

        counts = Counter(self.votes.values())

        highest = max(counts.values())

        winners = [
            player
            for player, count in counts.items()
            if count == highest
        ]

        # Tie
        if len(winners) > 1:
            return None, True

        eliminated = winners[0]

        self.dead_players.add(eliminated)
        self.alive_players.remove(eliminated)

        return eliminated, False

    def reset_votes(self):
        """
        Clear votes after each meeting.
        """
        self.votes.clear()

    def is_alive(self, player):
        return player in self.alive_players

    def is_dead(self, player):
        return player in self.dead_players

    def get_alive_players(self):
        return sorted(list(self.alive_players))

    def get_dead_players(self):
        return sorted(list(self.dead_players))

    def alive_count(self):
        return len(self.alive_players)

    def dead_count(self):
        return len(self.dead_players)