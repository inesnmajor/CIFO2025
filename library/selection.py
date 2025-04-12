import random
from copy import deepcopy
def tournament_selection(population, k=5):
    # randomly sample k individuals from the population
    # select the one with the highest fitness among them
    return deepcopy(max(random.sample(population, k), key=lambda s: s.fitness()))

def fitness_proportionate_selection(population):
    fitness_values = [ind.fitness() for ind in population]
    total_fitness = sum(fitness_values)
    if total_fitness == 0:
            # if all individuals have zero fitness, return a random one
        return deepcopy(random.choice(population))
    
    # spin the roulette wheel: choose a random value between 0 and total fitness
    rand = random.uniform(0, total_fitness)

    # traverse the population and accumulate fitness until surpassing the random threshold
    cumulative = 0
    for ind, fit in zip(population, fitness_values):
        cumulative += fit
        if rand <= cumulative:
            return deepcopy(ind)
