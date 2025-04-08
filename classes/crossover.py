import random
from selection import FootballSolution, N_TEAMS

def team_swap_crossover(self, p1, p2):
    point = random.randint(1, N_TEAMS - 1)
    c1_repr = p1.repr[:point] + p2.repr[point:]
    c2_repr = p2.repr[:point] + p1.repr[point:]
    return FootballSolution(c1_repr), FootballSolution(c2_repr)

def team_two_point_crossover(self, p1, p2):
    from copy import deepcopy

    # Selecionar dois pontos de corte distintos
    points = sorted(random.sample(range(1, N_TEAMS), 2))
    p1a, p1b = points

    # Fazer cópias das representações
    p1_repr = deepcopy(p1.repr)
    p2_repr = deepcopy(p2.repr)

    # Criar novos filhos com 2 pontos de corte
    c1_repr = p1_repr[:p1a] + p2_repr[p1a:p1b] + p1_repr[p1b:]
    c2_repr = p2_repr[:p1a] + p1_repr[p1a:p1b] + p2_repr[p1b:]

    # Construir soluções
    c1 = FootballSolution(repr=c1_repr)
    c2 = FootballSolution(repr=c2_repr)

    return c1, c2