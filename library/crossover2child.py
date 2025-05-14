from copy import deepcopy
from collections import Counter
from library.classes import FootballSolution, Team
from library.fixed_para import POSITIONS, TEAM_STRUCTURE, N_TEAMS,TEAM_SIZE, players_df,MAX_BUDGET
import random
import numpy as np

def crossover_position_based_two_offspring(p1: FootballSolution, p2: FootballSolution) -> tuple[FootballSolution, FootballSolution]:
    '''
    For each team, combines players from both parents while respecting positional structure (1 GK, 2 DEF, 2 MID, 2 FWD).
    the same as the 1 child crossover but adapted to 2 children
    '''
    expected_structure = TEAM_STRUCTURE
    name_to_player = {p['Name']: p for _, p in players_df.iterrows()}
    all_names = set(name_to_player.keys())

    offspring_teams_1 = []
    offspring_teams_2 = []
    used_names_1 = set()
    used_names_2 = set()

    #build both offspring in parallel
    for team_idx in range(N_TEAMS):
        for offspring_label, offspring_teams, used_names in [
            ("Filho 1", offspring_teams_1, used_names_1),
            ("Filho 2", offspring_teams_2, used_names_2)
        ]:
            team_players = []
            position_pool = {pos: [] for pos in expected_structure}
            
            #gather player pool from both parents for this team
            for parent in [p1, p2]:
                for player in parent.repr[team_idx].players:
                    position_pool[player['Position']].append(player)

            # fill the team position by position
            for pos, n_needed in expected_structure.items():
                selected = []
                pool = position_pool[pos]
                random.shuffle(pool) #introduce variability

                # select from parents
                for p in pool:
                    if p['Name'] in used_names:
                        continue
                    selected.append(p)
                    used_names.add(p['Name'])
                    if len(selected) == n_needed:
                        break

                # fill with dataset if needed
                if len(selected) < n_needed:
                    available = [name_to_player[n] for n in all_names - used_names if name_to_player[n]['Position'] == pos]
                    random.shuffle(available)
                    for p in available:
                        selected.append(p)
                        used_names.add(p['Name'])
                        if len(selected) == n_needed:
                            break

                if len(selected) < n_needed:
                    raise SystemExit(f"[{offspring_label}] Team structure violation {team_idx+1}")

                team_players.extend(selected)

            offspring_teams.append(Team(team_players))

    return (
        FootballSolution(offspring_teams_1, players_df),
        FootballSolution(offspring_teams_2, players_df)
    )


def crossover_blockwise_teams_two_offspring(p1: FootballSolution, p2: FootballSolution) -> tuple[FootballSolution, FootballSolution]:
    '''
    Each offspring inherits a random block of teams from each parent (e.g., 3 from p1, 2 from p2).
    Resolves duplicated players by filling missing spots with available players.
    Ensures valid team structures for both offspring. The same as the 1 child but adapted to 2 children
    '''
    from copy import deepcopy
    expected_structure = {'GK': 1, 'DEF': 2, 'MID': 2, 'FWD': 2}
    name_to_player = {p['Name']: p for _, p in players_df.iterrows()}
    all_names = set(name_to_player.keys())

    def generate_offspring():
        used_names = set()
        offspring_teams = []
        #randomly decide how many teams to take from p1
        n_from_p1 = random.randint(2, 3)
        p1_indices = random.sample(range(N_TEAMS), n_from_p1)
        p2_indices = [i for i in range(N_TEAMS) if i not in p1_indices]

        #iterate through selected indices from both parents
        for idx in p1_indices + p2_indices:
            source = p1 if idx in p1_indices else p2
            raw_players = deepcopy(source.repr[idx].players)
            team_players = [p for p in raw_players if p['Name'] not in used_names]
            used_names.update(p['Name'] for p in team_players)

            # fill missing players if team is incomplete
            if len(team_players) < TEAM_SIZE:
                pos_counts = Counter(p['Position'] for p in team_players)
                pos_missing = {pos: expected_structure[pos] - pos_counts.get(pos, 0) for pos in expected_structure}
                for pos, count in pos_missing.items():
                    if count > 0:
                        available = [name_to_player[n] for n in all_names - used_names if name_to_player[n]['Position'] == pos]
                        random.shuffle(available)
                        team_players.extend(available[:count])
                        used_names.update(p['Name'] for p in available[:count])

            offspring_teams.append(Team(team_players))
        return FootballSolution(offspring_teams, players_df)

    return generate_offspring(), generate_offspring()
