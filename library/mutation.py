import random

def mutate_swap_between_teams(self, solution):
    from copy import deepcopy
    new_repr = deepcopy(solution.repr)
    team_indices = random.sample(range(len(new_repr)), 2)
    t1, t2 = new_repr[team_indices[0]], new_repr[team_indices[1]]

    positions1 = {p['Position'] for p in t1.players}
    positions2 = {p['Position'] for p in t2.players}
    common_positions = list(positions1 & positions2)
    if not common_positions:
        return solution

    pos = random.choice(common_positions)
    p1_candidates = [i for i, p in enumerate(t1.players) if p['Position'] == pos]
    p2_candidates = [i for i, p in enumerate(t2.players) if p['Position'] == pos]

    if not p1_candidates or not p2_candidates:
        return solution

    i1 = random.choice(p1_candidates)
    i2 = random.choice(p2_candidates)

    t1.players[i1], t2.players[i2] = t2.players[i2], t1.players[i1]

    if t1.is_valid() and t2.is_valid():
        final_solution = solution.__class__(repr=new_repr)
        if is_unique(final_solution):
            return final_solution
    return solution
    
def mutate_global_position_permutation(self, solution, position='DEF'):
    from copy import deepcopy
    new_repr = deepcopy(solution.repr)
    all_players = [p for team in new_repr for p in team.players if p['Position'] == position]
    if len(all_players) != 2 * len(new_repr):
        return solution

    random.shuffle(all_players)
    idx = 0
    for team in new_repr:
        count = 0
        for i, p in enumerate(team.players):
            if p['Position'] == position and count < 2:
                team.players[i] = all_players[idx]
                idx += 1
                count += 1

    if all(team.is_valid() for team in new_repr):
        final_solution = solution.__class__(repr=new_repr)
        if is_unique(final_solution):
            return final_solution
    return solution


def mutate_random_position_swap(self, solution):
    from copy import deepcopy
    new_repr = deepcopy(solution.repr)
    t1, t2 = random.sample(range(len(new_repr)), 2)

    players1 = new_repr[t1].players
    players2 = new_repr[t2].players

    possible_pairs = [(i, j) for i in range(len(players1)) for j in range(len(players2))
                    if players1[i]['Position'] == players2[j]['Position']]
    if not possible_pairs:
        return solution

    i1, i2 = random.choice(possible_pairs)
    players1[i1], players2[i2] = players2[i2], players1[i1]

    if new_repr[t1].is_valid() and new_repr[t2].is_valid():
        final_solution = solution.__class__(repr=new_repr)
        if is_unique(final_solution):
            return final_solution
    return solution


def is_unique(solution):
    all_names = [p['Name'] for team in solution.repr for p in team.players]
    return len(all_names) == len(set(all_names))
