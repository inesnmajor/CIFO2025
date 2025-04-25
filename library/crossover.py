from copy import deepcopy
from collections import Counter
from library.classes import FootballSolution, Team
from library.fixed_para import POSITIONS, TEAM_STRUCTURE, N_TEAMS,TEAM_SIZE, players_df,MAX_BUDGET
import random

def crossover_by_team_with_repair(p1: FootballSolution, p2: FootballSolution) -> FootballSolution:
    """
    Team-wise crossover: randomly pick teams from parents, 
    repair duplicates and missing players, and fix budget violations if needed.
    """
    offspring_teams = []
    used_names = set()

    # Step 1: Randomly select teams from parents
    for i in range(N_TEAMS):
        team_source = p1 if random.random() < 0.5 else p2
        team = deepcopy(team_source.repr[i])
        offspring_teams.append(team)
        used_names.update(p['Name'] for p in team.players)

    # Step 2: Detect and remove duplicate players
    all_players = [p['Name'] for team in offspring_teams for p in team.players]
    name_counts = Counter(all_players)
    duplicates = [name for name, count in name_counts.items() if count > 1]

    for name in duplicates:
        found_once = False
        for team in offspring_teams:
            new_players = []
            for p in team.players:
                if p['Name'] == name:
                    if not found_once:
                        new_players.append(p)
                        found_once = True  # Keep first occurrence
                else:
                    new_players.append(p)
            team.players = new_players

    # Step 3: Fill missing players
    name_to_player = {p['Name']: p for _, p in players_df.iterrows()}
    all_names = set(players_df['Name'])
    all_used = {p['Name'] for team in offspring_teams for p in team.players}
    missing_names = list(all_names - all_used)

    for name in missing_names:
        player = name_to_player[name]
        for team in offspring_teams:
            pos = player['Position']
            pos_count = sum(1 for p in team.players if p['Position'] == pos)
            if len(team.players) < TEAM_SIZE and pos_count < TEAM_STRUCTURE[pos]:
                team.players.append(player)
                break

    # Step 4: Fix overbudget teams (new!)
    for team in offspring_teams:
        if team.total_salary() > MAX_BUDGET:
            # Find cheaper players to replace expensive ones
            available_players = [
                p for p in players_df.to_dict('records')
                if p['Name'] not in {pl['Name'] for t in offspring_teams for pl in t.players}
            ]

            for _ in range(5):  # attempt up to 5 replacements per team
                most_expensive = max(team.players, key=lambda p: p['Salary (€M)'])
                pos = most_expensive['Position']

                # Find cheaper candidates with the same position
                cheaper_candidates = [p for p in available_players if p['Position'] == pos and p['Salary (€M)'] < most_expensive['Salary (€M)']]

                if not cheaper_candidates:
                    break  # no cheaper replacement found

                replacement = random.choice(cheaper_candidates)
                team.players.remove(most_expensive)
                team.players.append(replacement)

                available_players.remove(replacement)

                if team.total_salary() <= MAX_BUDGET:
                    break  # team budget is now okay

    # Step 5: Return final offspring
    if all(team.is_valid() for team in offspring_teams):
        return FootballSolution(offspring_teams, players_df)
    else:
        return deepcopy(p1)  # fallback if fixing fails




def crossover_teamwise_mix_and_repair(p1: FootballSolution, p2: FootballSolution) -> FootballSolution:
    """
    Team-wise crossover: mix players from parents, repair duplicates, 
    and fix teams that exceed the budget by replacing expensive players.
    """
    offspring_teams = []
    used_names = set()

    # Step 1: Mix players team by team
    for i in range(N_TEAMS):
        team1_players = deepcopy(p1.repr[i].players)
        team2_players = deepcopy(p2.repr[i].players)

        random.shuffle(team1_players)
        random.shuffle(team2_players)

        half = TEAM_SIZE // 2
        team_players = team1_players[:half] + team2_players[TEAM_SIZE - half:]
        offspring_teams.append(Team(team_players))
        used_names.update(p['Name'] for p in team_players)

    # Step 2: Detect and remove duplicate players
    all_players = [p['Name'] for team in offspring_teams for p in team.players]
    name_counts = Counter(all_players)
    duplicates = [name for name, count in name_counts.items() if count > 1]

    for name in duplicates:
        found_once = False
        for team in offspring_teams:
            new_players = []
            for p in team.players:
                if p['Name'] == name:
                    if not found_once:
                        new_players.append(p)
                        found_once = True
                else:
                    new_players.append(p)
            team.players = new_players

    # Step 3: Fill missing players
    name_to_player = {p['Name']: p for _, p in players_df.iterrows()}
    all_names = set(players_df['Name'])
    all_used = {p['Name'] for team in offspring_teams for p in team.players}
    missing_names = list(all_names - all_used)

    for name in missing_names:
        player = name_to_player[name]
        for team in offspring_teams:
            pos = player['Position']
            pos_count = sum(1 for p in team.players if p['Position'] == pos)
            if len(team.players) < TEAM_SIZE and pos_count < TEAM_STRUCTURE[pos]:
                team.players.append(player)
                break

    # Step 4: Repair overbudget teams
    for team in offspring_teams:
        while team.total_salary() > MAX_BUDGET:
            # Find the most expensive player in the team
            most_expensive_player = max(team.players, key=lambda p: p['Salary (€M)'])
            pos = most_expensive_player['Position']

            # Find cheaper candidates for the same position from the available dataset
            candidates = players_df[(players_df['Position'] == pos) &
                                    (~players_df['Name'].isin([p['Name'] for p in team.players])) &
                                    (players_df['Salary (€M)'] < most_expensive_player['Salary (€M)'])]

            if candidates.empty:
                # No cheaper replacement found, cannot repair further
                break

            # Replace with the cheapest candidate available
            cheapest_candidate = candidates.sort_values('Salary (€M)').iloc[0].to_dict()
            team.players.remove(most_expensive_player)
            team.players.append(cheapest_candidate)

    # Step 5: Final validation
    if all(team.is_valid() for team in offspring_teams):
        return FootballSolution(offspring_teams, players_df)
    else:
        return deepcopy(p1)







