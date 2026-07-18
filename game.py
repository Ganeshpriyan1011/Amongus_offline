# game.py

from roles import RoleManager
from tasks import TaskManager
from voting import VotingManager


class GameManager:

    def __init__(self):

        self.role_manager = RoleManager()
        self.task_manager = TaskManager()
        self.voting_manager = VotingManager()

        self.roles = {}
        self.tasks = {}

        self.started = False
        self.mediator = None
        self.dead_body_reported = False
        self.reported_by = None
        self.victim = None
        self.location = None

    def start_game(self, players, mediator=None, custom_tasks=None):

        if len(players) < 4:
            raise ValueError("Minimum 4 players required.")

        self.mediator = mediator if mediator else None

        # Assign roles
        self.roles = self.role_manager.assign_roles(
            players,
            mediator
        )

        # Assign tasks
        self.tasks = self.task_manager.assign_tasks(
            self.roles,
            custom_tasks
        )

        # Initialize voting
        self.voting_manager.initialize_players(
            list(self.roles.keys())
        )

        self.started = True
        self.dead_body_reported = False
        self.reported_by = None
        self.victim = None
        self.location = None

    def get_role(self, player):
        return self.roles.get(player)

    def get_task(self, player):
        return self.tasks.get(player)

    def reveal_player(self, player):

        if player not in self.roles:
            return None

        return {
            "role": self.roles[player],
            "task": self.tasks[player]
        }

    def report_dead_body(self, reporter, victim, location):
        """Report a dead body and trigger emergency meeting"""
        if not self.started:
            return False, "Game has not started."
        
        if reporter not in self.roles:
            return False, "Player not found."
        
        if reporter in self.voting_manager.get_dead_players():
            return False, "Dead players cannot report bodies."
        
        if self.dead_body_reported:
            return False, "A body has already been reported."
        
        if victim not in self.roles:
            return False, "Victim not found in game."
        
        self.dead_body_reported = True
        self.reported_by = reporter
        self.victim = victim
        self.location = location
        return True, f"{reporter} reported {victim}'s body at {location}! Emergency meeting called!"

    def vote(self, voter, voted_player):
        return self.voting_manager.cast_vote(
            voter,
            voted_player
        )

    def end_meeting(self):

        eliminated, tie = self.voting_manager.eliminate_player()

        votes = self.voting_manager.vote_count()

        self.voting_manager.reset_votes()
        self.dead_body_reported = False
        self.reported_by = None
        self.victim = None
        self.location = None

        return eliminated, tie, votes

    def get_alive_players(self):
        return self.voting_manager.get_alive_players()

    def get_dead_players(self):
        return self.voting_manager.get_dead_players()

    def winner(self):

        alive = self.get_alive_players()

        crew = 0
        impostors = 0

        for player in alive:

            if self.roles[player] == "Crewmate":
                crew += 1
            else:
                impostors += 1

        if impostors == 0:
            return "Crewmates"

        if impostors >= crew:
            return "Impostors"

        return None

    def get_roles(self):
        return self.roles

    def is_body_reported(self):
        return self.dead_body_reported

    def get_reporter(self):
        return self.reported_by

    def get_victim(self):
        return self.victim

    def get_location(self):
        return self.location

    def kill_player(self, player):
        """Mark a player as dead (killed by impostor)"""
        if not self.started:
            return False, "Game has not started."
        
        if player not in self.roles:
            return False, "Player not found."
        
        if player in self.voting_manager.get_dead_players():
            return False, f"{player} is already dead."
        
        self.voting_manager.dead_players.add(player)
        if player in self.voting_manager.alive_players:
            self.voting_manager.alive_players.remove(player)
        
        return True, f"{player} has been killed."

    def reset(self):

        self.started = False

        self.roles.clear()
        self.tasks.clear()

        self.role_manager.clear_roles()

        self.voting_manager.votes.clear()
        self.voting_manager.dead_players.clear()
        self.voting_manager.alive_players.clear()

        self.mediator = None
        self.dead_body_reported = False
        self.reported_by = None
        self.victim = None
        self.location = None
