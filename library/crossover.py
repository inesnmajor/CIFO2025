from copy import deepcopy
from collections import Counter
from library.classes import FootballSolution, Team
from library.fixed_para import POSITIONS, TEAM_STRUCTURE, N_TEAMS,TEAM_SIZE, players_df
import random

def crossover_by_team_with_repair(p1: FootballSolution, p2: FootballSolution):
    
    used_names = set()
    offspring_teams = []

    for i in range(N_TEAMS):
        team_source = p1 if random.random() < 0.5 else p2
        team = deepcopy(team_source.repr[i])
        offspring_teams.append(team)
        used_names.update(p['Name'] for p in team.players)

    all_names = set(players_df['Name'])
    name_to_player = {p['Name']: p for _, p in players_df.iterrows()}
    all_names_in_child = [p['Name'] for t in offspring_teams for p in t.players]
    name_counts = Counter(all_names_in_child)
    duplicates = [name for name, count in name_counts.items() if count > 1]
    faltam = list(all_names - set(all_names_in_child))

    for name in duplicates:
        found_once = False
        for team in offspring_teams:
            # filtra os jogadores da equipa mantendo só 1 com esse nome
            new_players = []
            for p in team.players:
                if p['Name'] == name:
                    if not found_once:
                        new_players.append(p)
                        found_once = True
                    # ignora os restantes
                else:
                    new_players.append(p)
            team.players = new_players


    for missing_name in faltam:
        player = name_to_player[missing_name]
        for team in offspring_teams:
            pos = player['Position']
            count = sum(1 for p in team.players if p['Position'] == pos)
            if count < TEAM_STRUCTURE[pos]:
                team.players.append(player)
                break

    if all(t.is_valid() for t in offspring_teams):
        return FootballSolution(offspring_teams, players_df)
    else:
        return deepcopy(p1)



def crossover_by_position(p1: FootballSolution, p2: FootballSolution) -> FootballSolution:
    # Step 1: collect unique players per position from both parents
    position_pool = {pos: {} for pos in POSITIONS}
    for pos in POSITIONS:
        for team in p1.repr + p2.repr:
            for player in team.players:
                if player['Position'] == pos:
                    position_pool[pos][player['Name']] = player  # remove duplicates

    # Step 2: sample exactly the number of players needed per position
    selected_by_position = {}
    for pos in POSITIONS:
        total_needed = TEAM_STRUCTURE[pos] * N_TEAMS
        candidates = list(position_pool[pos].values())
        random.shuffle(candidates)
        selected_by_position[pos] = candidates[:total_needed]

    # Step 3: construct N_TEAMS teams with correct structure
    teams = []
    indices = {pos: 0 for pos in POSITIONS}

    for _ in range(N_TEAMS):
        team_players = []
        for pos in POSITIONS:
            for _ in range(TEAM_STRUCTURE[pos]):
                player = selected_by_position[pos][indices[pos]]
                team_players.append(player)
                indices[pos] += 1
        teams.append(Team(team_players))

    return FootballSolution(teams, players_df)






