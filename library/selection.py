import random
from copy import deepcopy
def tournament_selection(population, k=3):
    return deepcopy(max(random.sample(population, k), key=lambda s: s.fitness()))

def fitness_proportionate_selection(population):
    fitness_values = [ind.fitness() for ind in population]
    total_fitness = sum(fitness_values)
    if total_fitness == 0:
        return deepcopy(random.choice(population))
    rand = random.uniform(0, total_fitness)
    cumulative = 0
    for ind, fit in zip(population, fitness_values):
        cumulative += fit
        if rand <= cumulative:
            return deepcopy(ind)
