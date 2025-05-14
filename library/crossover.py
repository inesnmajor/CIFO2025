from copy import deepcopy
from collections import Counter
from library.classes import FootballSolution, Team
from library.fixed_para import POSITIONS, TEAM_STRUCTURE, N_TEAMS,TEAM_SIZE, players_df,MAX_BUDGET
import random
import numpy as np


def crossover_position_based(p1: FootballSolution, p2: FootballSolution) -> FootballSolution:
    """
    This operator builds offspring by combining players from two parent solutions while strictly respecting team structure (1 GK, 2 DEF, 2 MID, 2 FWD) 
    and avoiding duplicate players across teams. For each team, it first selects players from both parents' corresponding teams by position. 
    If not enough valid players are available, it completes the team with available players from the global pool. This ensures that all offspring teams 
    are valid and structurally complete.
    """
    expected_structure = {'GK': 1, 'DEF': 2, 'MID': 2, 'FWD': 2}
    name_to_player = {p['Name']: p for _, p in players_df.iterrows()}
    all_names = set(name_to_player.keys())
    offspring_teams = []
    used_names = set()  

    for team_idx in range(N_TEAMS):
        team_players = []

        # group by parents position
        position_pool = {'GK': [], 'DEF': [], 'MID': [], 'FWD': []}
        for parent in [p1, p2]:
            for p in parent.repr[team_idx].players:
                position_pool[p['Position']].append(p)

        # select players by pos.
        for pos, n_needed in expected_structure.items():
            pool = position_pool[pos]
            random.shuffle(pool)
            selected = []

            # trying from parents
            for p in pool:
                if p['Name'] not in used_names:
                    selected.append(p)
                    used_names.add(p['Name'])
                    if len(selected) == n_needed:
                        break

            # if missing complete with free players 
            if len(selected) < n_needed:
                available = [name_to_player[n] for n in all_names - used_names if name_to_player[n]['Position'] == pos]
                random.shuffle(available)
                for p in available:
                    selected.append(p)
                    used_names.add(p['Name'])
                    if len(selected) == n_needed:
                        break

            if len(selected) < n_needed:
                print(f"ERROR: Could not fill {n_needed} players in position {pos} for team {team_idx+1}")
                raise SystemExit("Structure violation even after attempting to fill with available players.")

            team_players.extend(selected)

        offspring_teams.append(Team(team_players))
        

    return FootballSolution(offspring_teams, players_df)


def crossover_blockwise_teams(p1: FootballSolution, p2: FootballSolution) -> FootballSolution:
    """
    This operator creates offspring by randomly selecting a number of complete teams from each parent (e.g., 3 from one parent, 2 from the other). 
    After inheriting these teams, it checks for duplicate players across teams and resolves any conflicts by replacing 
    duplicates with valid, available players from the global player pool. The operator ensures that all teams in the offspring maintain the required 
    structure and contain unique players.
    """
    from copy import deepcopy

    name_to_player = {p['Name']: p for _, p in players_df.iterrows()}
    all_names = set(name_to_player.keys())
    used_names = set()
    offspring_teams = []

    # randomly decide how many teams to take from p1 (e.g., 2 or 3)
    n_from_p1 = random.randint(2, 3)
    p1_indices = random.sample(range(N_TEAMS), n_from_p1)
    p2_indices = [i for i in range(N_TEAMS) if i not in p1_indices]


    # teams from p1
    for i in p1_indices:
        team_players = deepcopy(p1.repr[i].players)
        offspring_teams.append(Team(team_players))
        used_names.update(p['Name'] for p in team_players)

    # teams from p2
    for i in p2_indices:
        team_players = []
        for p in p2.repr[i].players:
            if p['Name'] not in used_names:
                team_players.append(deepcopy(p))
                used_names.add(p['Name'])
        #if team is incomplete due to removed duplicates, fill remaining slots
        if len(team_players) < TEAM_SIZE:
            positions_needed = Counter(TEAM_STRUCTURE)
            for p in team_players:
                positions_needed[p['Position']] -= 1

            # fill remaining positions with available players not yet used
            for pos, count in positions_needed.items():
                available = [name_to_player[n] for n in all_names - used_names if name_to_player[n]['Position'] == pos]
                random.shuffle(available)
                team_players.extend(available[:count])
                used_names.update(p['Name'] for p in available[:count])

        offspring_teams.append(Team(team_players))

    
    return FootballSolution(offspring_teams, players_df)




