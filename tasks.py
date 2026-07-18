# tasks.py

import random


class TaskManager:
    def __init__(self):

        # Tasks for Crewmates
        self.crewmate_tasks = [
            "Fill the water bottle",
            "Say hi to every teammate",
            "Take care of the mediator",
            "Visit the library entrance",
            "Touch three classroom doors",
            "Visit the notice board",
            "Walk one round of the department",
            "Throw a piece of litter into the dustbin",
            "Visit the drinking water area",
            "Count 20 steps in the corridor",
            "Touch the department name board",
            "Visit the staircase and return",
            "Stand near the lab entrance for 10 seconds",
            "Walk to the canteen entrance",
            "Check the classroom timetable",
            "Wave at a classmate",
            "Sit on another bench for one minute",
            "Walk around the parking area",
            "Visit the seminar hall entrance",
            "Count five windows in the corridor",
            "Read a notice for 15 seconds",
            "Touch the college gate",
            "Visit the office entrance",
            "Walk around the ground once",
            "Visit the lift area",
            "Find the nearest fire extinguisher",
            "Touch a classroom window",
            "Walk to the washroom entrance",
            "Stand silently for 20 seconds",
            "Walk to the nearest tree and return"
        ]

        # Fake tasks for Impostors
        self.impostor_tasks = [
            "Pretend to check the notice board",
            "Walk around the corridor casually",
            "Visit the staircase",
            "Pretend to tie your shoelace",
            "Stand near the library for 15 seconds",
            "Walk to the canteen entrance",
            "Visit the water area",
            "Pretend to look for someone",
            "Read a poster for 20 seconds",
            "Walk to the parking area and return",
            "Stand near the department entrance",
            "Touch a classroom door and return",
            "Walk to the office entrance",
            "Visit the seminar hall",
            "Count ten floor tiles"
        ]

    def assign_tasks(self, roles, custom_tasks=None):

        tasks = {}

        # Use custom tasks if provided, otherwise use default
        if custom_tasks:
            crew_pool = custom_tasks["crewmate"].copy()
            imp_pool = custom_tasks["impostor"].copy()
        else:
            crew_pool = self.crewmate_tasks.copy()
            imp_pool = self.impostor_tasks.copy()

        random.shuffle(crew_pool)
        random.shuffle(imp_pool)

        for player, role in roles.items():

            if role == "Crewmate":

                if not crew_pool:
                    raise Exception(
                        "Not enough crewmate tasks available."
                    )

                tasks[player] = crew_pool.pop()

            else:

                if not imp_pool:
                    raise Exception(
                        "Not enough impostor tasks available."
                    )

                tasks[player] = imp_pool.pop()

        return tasks
