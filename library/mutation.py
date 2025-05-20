import random
'''
This mutation operator swaps two players with the same position between two randomly 
selected teams in the solution. The swap only happens if both teams remain valid after the 
exchange and the resulting solution is unique. 
If not, the original solution is returned unchanged. 
'''
def mutate_swap_between_teams(self, solution):
    from copy import deepcopy
    
    new_repr = deepcopy(solution.repr)
    # randomly select two distinct teams from the solution
    team_indices = random.sample(range(len(new_repr)), 2)
    t1, t2 = new_repr[team_indices[0]], new_repr[team_indices[1]]

    # identify the set of positions in each team
    positions1 = {p['Position'] for p in t1.players}
    positions2 = {p['Position'] for p in t2.players}
    common_positions = list(positions1 & positions2)
    if not common_positions:
        # if no common positions exist, return the original solution (mutation fails)
        #this is not suppose to happen, but it´s another layer of protection
        return solution

    # randomly select one of the shared positions
    pos = random.choice(common_positions)
    # find candidate players in both teams who play that position
    p1_candidates = [i for i, p in enumerate(t1.players) if p['Position'] == pos]
    p2_candidates = [i for i, p in enumerate(t2.players) if p['Position'] == pos]

    # if no candidates are found in either team, return the original solution
    #again, another protection
    if not p1_candidates or not p2_candidates:
        return solution

    # randomly choose one player from each team with the selected position
    i1 = random.choice(p1_candidates)
    i2 = random.choice(p2_candidates)

    # swap the players between the two teams
    t1.players[i1], t2.players[i2] = t2.players[i2], t1.players[i1]

    # validate the teams after the swap
    if t1.is_valid() and t2.is_valid():
        # recreate the solution with the modified representation
        final_solution = solution.__class__(repr=new_repr)
        # ensure the new solution is unique in the population
        if is_unique(final_solution):
            return final_solution
    
    # if mutation is invalid or not unique, return the original solution
    return solution

'''
This mutation operator randomly selects a player position and performs a global permutation of 
all players with that position across teams except the GK. 
It ensures that exactly two players of that position are reassigned per team. The mutation is only applied if all teams 
remain valid and the new solution is unique. Otherwise, the original solution is returned.
'''
#POR GK   
def mutate_global_position_permutation(self, solution):
    from copy import deepcopy
    
    new_repr = deepcopy(solution.repr)

    # choose a random position present in the solution
    all_positions = {p['Position'] for team in new_repr for p in team.players}
    if not all_positions:
        return solution
    position = random.choice(list(all_positions))

    # cet all players with the selected position
    all_players = [p for team in new_repr for p in team.players if p['Position'] == position]
    
    # check if we have exactly 2 per team to ensure it's valid
    if len(all_players) != 2 * len(new_repr):
        return solution

    # shuffle and reassign two players per team
    random.shuffle(all_players)
    idx = 0
    for team in new_repr:
        count = 0
        for i, p in enumerate(team.players):
            if p['Position'] == position and count < 2:
                team.players[i] = all_players[idx]
                idx += 1
                count += 1

    # return new solution if valid and unique
    if all(team.is_valid() for team in new_repr):
        final_solution = solution.__class__(repr=new_repr)
        if is_unique(final_solution):
            return final_solution
    return solution



'''
This mutation operator randomly selects two different teams and swaps one player between them, 
ensuring both players play the same position. The swap is only applied if both resulting teams 
remain valid and the new solution is unique. If not, the original solution is returned unchanged.
'''
def mutate_random_position_swap(self, solution):
    from copy import deepcopy
    new_repr = deepcopy(solution.repr)
    # randomly select two different teams
    t1, t2 = random.sample(range(len(new_repr)), 2)

    # get the list of players from each team
    players1 = new_repr[t1].players
    players2 = new_repr[t2].players

    # generate all possible pairs of player indices (i, j)
    # where the players from both teams play in the same position
    possible_pairs = [(i, j) for i in range(len(players1)) for j in range(len(players2))
                    if players1[i]['Position'] == players2[j]['Position']]
    # if there are no players with matching positions, return the original solution
    if not possible_pairs:
        return solution

    # randomly select one valid pair of players to swap
    i1, i2 = random.choice(possible_pairs)
    players1[i1], players2[i2] = players2[i2], players1[i1]

    # validate both teams after the swap
    if new_repr[t1].is_valid() and new_repr[t2].is_valid():
        # recreate the solution with the updated representation
        final_solution = solution.__class__(repr=new_repr)
        if is_unique(final_solution):
            return final_solution
    return solution

#this function is another layer of protection from players being the same in various teams, just to be safe
def is_unique(solution):
    all_names = [p['Name'] for team in solution.repr for p in team.players]
    return len(all_names) == len(set(all_names)) #garantees a players doesnt show up in more than one team



