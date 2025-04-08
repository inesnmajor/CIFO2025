import random
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from copy import deepcopy

players_df = pd.read_csv("players(in).csv")

POSITIONS = ["GK", "DEF", "MID", "FWD"]
TEAM_STRUCTURE = {"GK": 1, "DEF": 2, "MID": 2, "FWD": 2}
TEAM_SIZE = 7
N_TEAMS = 5
MAX_BUDGET = 750

class Solution(ABC):
    def __init__(self, repr=None):
        if repr is None:
            repr = self.random_initial_representation()
        self.repr = repr

    def __repr__(self):
        return str(self.repr)

    @abstractmethod
    def fitness(self):
        pass

    @abstractmethod
    def random_initial_representation(self):
        pass


class Team:
    def __init__(self, players):
        self.players = players

    def is_valid(self):
        pos_count = {p: 0 for p in POSITIONS} #count players in each pos (start w/ 0)
        total_cost = 0
        for player in self.players:
            pos_count[player['Position']] += 1 #when a player is seen sums to the count
            total_cost += player['Salary (€M)'] #and sums their salary
        if any(pos_count[p] != TEAM_STRUCTURE[p] for p in POSITIONS):
            return False  #if any pos doesn't have exacly the right nº of players, its invalid
        if total_cost > MAX_BUDGET:
            return False  #if exceeds the budget, its false
        return True

    def average_skill(self):
        return np.mean([p['Skill'] for p in self.players]) #average skill of each team

class FootballSolution(Solution):
    def __init__(self, repr=None, players_df=players_df):
        self.players_df = players_df
        super().__init__(repr=repr)

##por equanto,, por no is valid---
    def _validate_repr(self, repr):
        if not isinstance(repr, list):
            raise TypeError("Representation must be a list of Team objects")
        if len(repr) != N_TEAMS:
            raise ValueError("There must be exactly 5 teams")
        for team in repr:
            if not isinstance(team, Team):
                raise TypeError("Each element in the representation must be a Team")
            if not team.is_valid():
                raise ValueError("Each team must be valid (positions + budget)")

    
    def random_initial_representation(self):
        #initial available players
        all_players = self.players_df.to_dict('records')
        random.shuffle(all_players) #shuffle players

        # group players by position
        by_position = {pos: [] for pos in POSITIONS}
        for p in all_players:
            if p['Position'] in by_position:
                by_position[p['Position']].append(p)

        # shuffle each group of positions
        for pos_list in by_position.values():
            random.shuffle(pos_list)

        teams = []
        used_names = set()

        attempts = 0
        max_attempts = 100  # security for infinite loops

        while len(teams) < N_TEAMS and attempts < max_attempts:
            attempts += 1

            try:
                team_players = []

                for pos, count in TEAM_STRUCTURE.items():
                    # filters for non used players
                    available = [p for p in by_position[pos] if p['Name'] not in used_names]
                    if len(available) < count:
                        raise ValueError("Not enough players left for position:", pos)
                    team_players.extend(random.sample(available, count))  # picks the players

                team = Team(team_players)

                if team.is_valid():
                    teams.append(team)
                    used_names.update(p['Name'] for p in team_players)

            except Exception as e:
                continue  # fails, and trys again

        if len(teams) != N_TEAMS:
            print("[INFO] Could not create enough valid teams. Retrying full generation...")
            return self.random_initial_representation()

        return teams



    def fitness(self):
        valid_teams = [team for team in self.repr if team.is_valid()]
        if len(valid_teams) < 2:
            return 0
        skills = [team.average_skill() for team in valid_teams]
        return 1 / (1 + np.std(skills)) #WE MUST USE THIS FUNCTION BC IF NOT THERE WILL BE PLAYERS IN MORE THAN 1 TEAM
    
   

    #-----
    def deepcopy(self):
        return deepcopy(self)