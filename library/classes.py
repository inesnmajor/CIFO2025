import random
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from copy import deepcopy
from library.fixed_para import POSITIONS,TEAM_SIZE,TEAM_STRUCTURE,N_TEAMS, MAX_BUDGET,players_df

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

    def __repr__(self):
        header = f"{'Player':<20} {'Position':<10} {'Skill':<6} {'Salary (€M)':<10}"
        lines = [header, "-" * len(header)]
        for p in self.players:
            line = f"{p['Name']:<20} {p['Position']:<10} {p['Skill']:<6.1f} {p['Salary (€M)']:<10.1f}"
            lines.append(line)
        summary = f"\nAverage Skill: {self.average_skill():.2f} | Total Salary: {self.total_salary():.2f}M | Valid: {self.is_valid()}"
        return "\n".join(lines) + summary

    def __len__(self):
        return len(self.players)

    def __getitem__(self, idx):
        return self.players[idx]
    
    def is_valid(self):
        pos_count = {p: 0 for p in POSITIONS} #count players in each pos (start w/ 0)
        #total_cost = 0
        for player in self.players:
            pos_count[player['Position']] += 1 #when a player is seen sums to the count
        if any(pos_count[p] != TEAM_STRUCTURE[p] for p in POSITIONS):
            return False  #if any pos doesn't have exacly the right nº of players, its invalid
        return True

    def average_skill(self):
        return np.mean([p['Skill'] for p in self.players])

    def total_salary(self):
        return sum(p['Salary (€M)'] for p in self.players)


    

class FootballSolution(Solution):
    def __init__(self, repr=None, players_df=players_df):
        self.players_df = players_df
        super().__init__(repr=repr)
    
    def __repr__(self):
        summary = f"\n===== FootballSolution =====\n"
        for idx, team in enumerate(self.repr, 1):
            summary += f"\n--- Team {idx} ---\n"
            for player in team.players:
                summary += (f"{player['Name']:<25} | {player['Position']:<3} | "
                            f"Skill: {player['Skill']:<5.1f} | €{player['Salary (€M)']:<6.1f}M\n")
        summary += f"\nFitness: {self.fitness():.4f}\n"
        return summary


    #this validates that the solution
    def _validate_repr(self, repr):
        if not isinstance(repr, list):
            raise TypeError("Representation must be a list of Team objects")
        if len(repr) != N_TEAMS:
            raise ValueError("There must be exactly 5 teams")
        for team in repr:
            if not isinstance(team, Team):
                raise TypeError("Each element in the representation must be a Team")
            if not team.is_valid():
                raise ValueError("Each team must be valid (positions and structure)")

    
    def random_initial_representation(self):
        all_players = self.players_df.to_dict('records')
        random.shuffle(all_players)

        # group players by their position
        by_position = {pos: [] for pos in POSITIONS}
        for p in all_players:
            if p['Position'] in by_position:
                by_position[p['Position']].append(p)
        #shuffle each position group to randomize selection within positions
        for pos_list in by_position.values():
            random.shuffle(pos_list)

        teams = []
        used_names = set()

        while len(teams) < N_TEAMS:
            try:
                team_players = []
                #for each required position, select the needed number of available players
                for pos, count in TEAM_STRUCTURE.items():
                    #only not used players
                    available = [p for p in by_position[pos] if p['Name'] not in used_names]
                    if len(available) < count:
                        raise ValueError(f"Not enough players left for position: {pos}") #extra verification
                    team_players.extend(random.sample(available, count))

                team = Team(team_players)

                if team.is_valid():
                    teams.append(team)
                    #mark these players as used
                    used_names.update(p['Name'] for p in team_players)

            except Exception:
                #if smth is wrong retry
                continue

        return teams

    def fitness(self):
        #ensure the representation is valid; otherwise, raise an error
        self._validate_repr(self.repr)  #let it raise ValueError naturally if invalid (layer of protection)

        #budget penalty
        penalty = 0
        for team in self.repr:
            excess = team.total_salary() - MAX_BUDGET
            if excess > 0:
                penalty += excess * 0.5  # weighted penalty

        #balance metric
        skills = [team.average_skill() for team in self.repr]
        base_score = 1 / (1 + np.std(skills))

        return max(0.001, base_score - penalty)
    


    

